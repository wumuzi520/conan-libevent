#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import shutil

class LibeventConan(ConanFile):
    name = "libevent"
    version = "2.0.22"
    url = "https://github.com/theirix/conan-libevent"
    description = 'libevent - an event notification library'
    license = "https://github.com/libevent/libevent/blob/release-%s-stable/LICENSE" % version
    website = "https://libevent.org"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "with_openssl": [True, False],
               "disable_threads": [True, False]}
    default_options = "shared=False", "with_openssl=True", "disable_threads=False"

    def config_options(self):
        del self.settings.compiler.libcxx
        if self.settings.os == "Windows":
            self.options.shared = False
            self.options.with_openssl = False

    def requirements(self):
        if self.options.with_openssl:
            self.requires.add("OpenSSL/[>1.0.2a,<1.0.3]@conan/stable", private=False)
            self.options["OpenSSL"].shared = self.options.shared

    def source(self):
        tools.get("https://github.com/libevent/libevent/releases/download/release-{0}-stable/libevent-{0}-stable.tar.gz".format(self.version))
        os.rename("libevent-{0}-stable".format(self.version), "sources")

    def build(self):

        if self.settings.os == "Linux" or self.settings.os == "Macos":

            env_build = AutoToolsBuildEnvironment(self)

            env_vars = env_build.vars.copy()
            # Configure script creates conftest that cannot execute without shared openssl binaries.
            # Ways to solve the problem:
            # 1. set *LD_LIBRARY_PATH (works with Linux but does not work on OS X 10.11 with SIP)
            # 2. copying dylib's to the build directory (fortunately works on OS X)
            # 3. set rpath (dangerous)
            imported_libs = []
            if self.options.with_openssl and self.options.shared:
                if self.settings.os == "Macos":
                    imported_libs = os.listdir(self.deps_cpp_info['OpenSSL'].lib_paths[0])
                    for imported_lib in imported_libs:
                        shutil.copy(self.deps_cpp_info['OpenSSL'].lib_paths[0] + '/' + imported_lib, "sources")
                    self.output.warn("Copying OpenSSL libraries to fix conftest")
                if self.settings.os == "Linux":
                    if 'LD_LIBRARY_PATH' in env_vars:
                        env_vars['LD_LIBRARY_PATH'] = ':'.join([env_vars['LD_LIBRARY_PATH']] + self.deps_cpp_info.libdirs)
                    else:
                        env_vars['LD_LIBRARY_PATH'] = ':'.join(self.deps_cpp_info.libdirs)

            # required to correctly find static libssl on Linux
            if self.options.with_openssl and self.settings.os == "Linux":
                env_vars['OPENSSL_LIBADD'] = '-ldl'

            # disable rpath build
            old_str = "-install_name \\$rpath/"
            new_str = "-install_name "
            tools.replace_in_file("sources/configure", old_str, new_str)

            # compose configure options
            suffix = ''
            if not self.options.shared:
                suffix += " --disable-shared "
            if self.options.with_openssl:
                suffix += "--enable-openssl "
            else:
                suffix += "--disable-openssl "
            if self.options.disable_threads:
                suffix += "--disable-thread-support "

            self.output.warn('Using env vars: ' + repr(env_vars))
            with tools.environment_append(env_vars):

                cmd = 'cd sources && ./configure %s' % (suffix)
                self.output.warn('Running: ' + cmd)
                self.run(cmd)

                cmd = 'cd sources && make'
                self.output.warn('Running: ' + cmd)
                self.run(cmd)

                # now clean imported libs
                if imported_libs:
                    for imported_lib in imported_libs:
                        os.unlink('sources/' + imported_lib)

        elif self.settings.os == "Windows":
            vcvars = tools.vcvars_command(self.settings)
            make_command = "nmake -f Makefile.nmake"
            with tools.chdir('sources'):
                self.run("%s && %s" % (vcvars, make_command))


    def package(self):
        self.copy("*.h", dst="include", src="sources/include")
        if self.settings.os == "Windows":
            # Windows build is not using configure, so event-config.h is copied from WIN32-Code folder
            self.copy("event-config.h", src="sources/WIN32-Code/event2", dst="include/event2")
            self.copy("tree.h", src="sources/WIN32-Code", dst="include")
            self.copy(pattern="*.lib", dst="lib", keep_path=False)
        for header in ['evdns', 'event', 'evhttp', 'evrpc', 'evutil']:
            self.copy(header+'.h', dst="include", src="sources")
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["rt"])

        if self.settings.os == "Windows":
            if not self.options.shared:
                self.cpp_info.libs.append('ws2_32')
