import os
import sys
import subprocess
import setuptools
import shutil
import tempfile
import logging
from zc.buildout.download import Download
import zc
import zc.recipe.egg

DOWNLOAD_URL = "http://projects.unbit.it/downloads/uwsgi-{0}.tar.gz"
MARKER = object()


def str_to_bool(s):
    """
    Converts a string to a bool value; looks at the first character,
    if it's y(es), t(rue) or 1 returns True, otherwise, False.
    """
    if len(s) > 0 and s[0] in "yYtT1":
        return True
    return False


class UWSGI:
    """
    Buildout recipe downloading, compiling and configuring python paths for uWSGI.
    """

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options["recipe"], options)
        self.name = name
        self.buildout = buildout
        self.log = logging.getLogger(self.name)

        global_options = buildout["buildout"]
        # Use the "download-cache" directory as cache, if present
        self.cache_dir = global_options.get("download-cache")

        if self.cache_dir is not None:
            # If cache_dir isn't an absolute path, make it relative to
            # buildout's directory
            if not os.path.isabs(self.cache_dir):
                self.cache_dir = os.path.join(global_options["directory"], self.cache_dir)

        self.use_system_binary = str_to_bool(options.get("use-system-binary", "false"))
        self.uwsgi_version = options.get("version", "latest")
        self.md5sum = options.get('md5sum') or None # empty string => None
        self.uwsgi_binary_path = os.path.join(global_options["bin-directory"], "uwsgi")

        # xml, ini
        self.config_file_format = options.get("output-format", "xml").lower()
        if self.config_file_format not in ["xml", "ini"]:
            self.log.warn("unknown output configuration format, defaulting to xml")
            self.config_file_format = "xml"

        if "extra-paths" in options:
            options["pythonpath"] = options["extra-paths"]
        else:
            options.setdefault("extra-paths", options.get("pythonpath", ""))

        self.output = options.setdefault("output",
                                         os.path.join(global_options["parts-directory"],
                                                      self.name,
                                                      "uwsgi.{0}".format(self.config_file_format)))
        self.options = options

    def download_release(self):
        """
        Download uWSGI release based on "version" option and return path to downloaded file.
        """
        if self.cache_dir is not None:
            download = Download(cache=self.cache_dir)
        else:
            self.log.warning("not using a download cache for uwsgi")
            download = Download()

        download_url = self.options.get("download-url", DOWNLOAD_URL)
        download_path, is_temp = download(
            download_url.format(self.uwsgi_version), md5sum=self.md5sum)
        return download_path

    def extract_release(self, download_path):
        """
        Extracts uWSGI package and returns path containing uwsgiconfig.py along with path to extraction root.
        """
        uwsgi_path = None
        extract_path = tempfile.mkdtemp("-uwsgi")
        setuptools.archive_util.unpack_archive(download_path, extract_path)
        for root, dirs, files in os.walk(extract_path):
            if "uwsgiconfig.py" in files:
                uwsgi_path = root
        return uwsgi_path, extract_path

    def build_uwsgi(self, uwsgi_path):
        """
        Build uWSGI and returns path to executable.
        """
        current_path = os.getcwd()
        profile = self.options.get("profile", MARKER)

        if profile is MARKER:
            profile = '%s/buildconf/default.ini' % uwsgi_path
        elif not os.path.isabs(profile):
            # if the specified profile is not an absolute path, try
            # looking for it in the buildout folder first; otherwise,
            # look for it in the current directory
            buildout_dir_profile = '%s/buildconf/%s' % (uwsgi_path, profile)
            if os.path.isfile(buildout_dir_profile):
                profile = buildout_dir_profile
            else:
                profile = os.path.abspath(profile)

        # Change dir to uwsgi_path for compile.
        os.chdir(uwsgi_path)
        build_stdout = tempfile.TemporaryFile()
        try:
            # Build uWSGI. We don't use the Makefile, since it uses an
            # override variable (with :=) we cannot specify the
            # Python interpreter we want to use.
            subprocess.check_call([self.options.get('executable', sys.executable),
                                   os.path.join(uwsgi_path, 'uwsgiconfig.py'),
                                   '--build',
                                   profile],
                                  stdout=build_stdout)
        finally:
            # Change back to original path.
            os.chdir(current_path)

        if os.path.isfile(self.uwsgi_binary_path):
            os.unlink(self.uwsgi_binary_path)

        shutil.copy(os.path.join(uwsgi_path, "uwsgi"), self.uwsgi_binary_path)

    def get_extra_paths(self):
        # Add libraries found by a site .pth files to our extra-paths.
        if 'pth-files' in self.options:
            import site
            for pth_file in self.options['pth-files'].splitlines():
                pth_libs = site.addsitedir(pth_file, set())
                if not pth_libs:
                    self.log.warning('No site *.pth libraries found for pth_file=%s' % pth_file)
                else:
                    self.log.info('Adding *.pth libraries=%s' % pth_libs)
                    self.options['extra-paths'] += '\n' + '\n'.join(pth_libs)

        # Add local extra-paths.
        return [p.replace('/', os.path.sep) for p in
                self.options['extra-paths'].splitlines() if p.strip()]

    def create_configuration_file(self):
        warned = False
        conf = []

        for key, value in self.options.items():

            if key.startswith("xml-") and len(key) > 4:
                if not warned:
                    self.log.warn("using 'xml-' options has been deprecated in favor of 'config-'. See documentation for details.")
                    warned = True

                key = key[4:]

            elif key.startswith("config-") and len(key) > 7:
                key = key[7:]
            else:
                continue

            if "\n" in value:
                for subvalue in value.splitlines():
                    conf.append((key, subvalue))
            else:
                conf.append((key, value))

        _, ws = self.egg.working_set()

        # get list of paths to put into pythonpath
        pythonpaths = ws.entries + self.get_extra_paths()

        # mungle basedir of pythonpath entries
        if 'pythonpath-eggs-directory' in self.options:
            source = self.options['eggs-directory']
            target = self.options['pythonpath-eggs-directory']
            pythonpaths = [path.replace(source, target) for path in pythonpaths]

        # generate pythonpath directives
        for path in pythonpaths:
            conf.append(("pythonpath", path))

        directory = os.path.dirname(self.output)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        if self.config_file_format == "xml":
            self.write_config_as_xml(conf)
        elif self.config_file_format == "ini":
            self.write_config_as_ini(conf)

        return self.output

    def write_config_as_xml(self, conf_options):
        conf = ""
        for key, value in conf_options:
            if value.lower() == "true":
                conf += "<{0}/>\n".format(key)
            elif value.lower() != "false":
                conf += "<{0}>{1}</{0}>\n".format(key, value)

        with open(self.output, "w") as f:
            f.write("<uwsgi>\n{0}</uwsgi>".format(conf))

    def write_config_as_ini(self, conf_options):
        conf = "[uwsgi]\n"
        for key, value in conf_options:
            conf += "{0} = {1}\n".format(key, value)
        with open(self.output, "w") as f:
            f.write(conf)

    def is_uwsgi_installed(self):
        if not os.path.isfile(self.uwsgi_binary_path):
            return False

        if self.uwsgi_version == 'latest':
            # If you ask for the latest version, we say we don't, in order to
            # force a download+recompile (since we can't know for sure if the package was
            # updated upstream or not)
            return False

        # Check the version
        process = subprocess.Popen([self.uwsgi_binary_path, '--version'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.strip() == self.uwsgi_version

    def install(self):
        paths = []
        if not self.use_system_binary:
            if not self.is_uwsgi_installed():
                # Download uWSGI.
                download_path = self.download_release()

                # Extract uWSGI.
                uwsgi_path, extract_path = self.extract_release(download_path)

                try:
                    # Build uWSGI.
                    self.build_uwsgi(uwsgi_path)
                finally:
                    # Remove extracted uWSGI package.
                    shutil.rmtree(extract_path)

            paths.append(self.uwsgi_binary_path)

        # Create uWSGI config file.
        paths.append(self.create_configuration_file())
        return paths

    update = install
