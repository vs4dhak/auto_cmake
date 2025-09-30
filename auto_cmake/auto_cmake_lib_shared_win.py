#!/usr/bin/env python

"""
Description: Generates a windows shared library
"""

__author__ = "Veda Sadhak"
__license__ = "MIT"

import os

from .auto_cmake import AutoCMake

class AutoCMakeLibSharedWin():

    def __init__(self, **cmake_config):

        # Creating instance
        self.ac = AutoCMake(**cmake_config)
        self.libs = cmake_config["libs"]

        if "jni_dir" in cmake_config.keys():
            self.jni_dir = cmake_config["jni_dir"]
        else:
            self.jni_dir = None

    def run(self):

        # Recursively adding all source
        for _dir in self.ac.include_dirs:
            self.ac.add_libraries(os.path.join(self.ac.proj_dir, _dir))
            self.ac.clear()

        # Adding the compile config
        self.ac.add("cmake_minimum_required(VERSION {})".format(self.ac.cmake_version))
        self.ac.add("project({} VERSION {})".format(self.ac.proj_name, self.ac.version))
        self.ac.add("set(CMAKE_CXX_STANDARD 11)")
        self.ac.add('set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")\n')

        # Setting flags
        self.ac.add('SET_PROPERTY(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS TRUE)\n')

        # Set headers and sources
        self.ac.add("set(SOURCES".format(self.ac.proj_name))
        for source in self.ac.sources:
            self.ac.add('    "{}"'.format(self.ac.get_posix_path(source)))
        for headers in self.ac.headers:
            self.ac.add('    "{}"'.format(self.ac.get_posix_path(headers)))
        self.ac.add(")\n")

        # Adding the shared lib
        self.ac.add("add_library({} SHARED {})\n".format(self.ac.proj_name, r"${SOURCES}"))

        # Setting flags
        self.ac.add("target_compile_definitions({} PUBLIC".format(self.ac.proj_name))
        for flag in self.ac.flags:
            self.ac.add('    {}'.format(flag))
        self.ac.add(")\n")

        # Add JNI libs
        if self.jni_dir:
            self.ac.add('include_directories("{}/include")'.format(self.jni_dir))
            self.ac.add('link_directories("{}/include")'.format(self.jni_dir))
            self.ac.add('include_directories("{}/include/win32")'.format(self.jni_dir))
            self.ac.add('link_directories("{}/include/win32")\n'.format(self.jni_dir))

        # Setting shared lib properties
        self.ac.add('set_target_properties({} PROPERTIES COMPILE_FLAGS "-fPIC")\n'.format(self.ac.proj_name))

        # Static linkage is required for successful Windows DLL creation.
        for lib in self.libs:
            self.ac.add('target_link_libraries({} {})\n'.format(self.ac.proj_name, self.ac.get_posix_path(lib)))

        # Adding include directories
        for include in self.ac.includes:
            if include not in self.ac.library_paths:
                self.ac.add('target_include_directories({} PUBLIC "{}")'.format(self.ac.proj_name, include))
        self.ac.add("")

        # Adding include directories
        for path in self.ac.library_paths:
            self.ac.add('target_include_directories({} PUBLIC "{}")'.format(self.ac.proj_name, path))
        self.ac.add("")

        # Writing main CMakeLists.txt
        self.ac.create_build_dir()
        self.ac.write(self.ac.build_dir)