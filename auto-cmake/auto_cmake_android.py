#!/usr/bin/env python

"""
Description: Generates an executable target
"""

__author__ = "Veda Sadhak"
__license__ = "MIT"
__version__ = "2023.03.01"

import os

from auto_cmake import AutoCMake

class AutoCMakeAndroid():

    def __init__(self, **cmake_config):

        # Creating instance
        self.ac = AutoCMake(**cmake_config)

        # Setting flags
        self.flags = cmake_config["flags"]

    def run(self):

        # Recursively adding all source
        for _dir in self.ac.include_dirs:
            self.ac.add_libraries(os.path.join(self.ac.proj_dir, _dir))
            self.ac.clear()

        # Adding the compile config
        self.ac.add("cmake_minimum_required(VERSION {})".format(self.ac.cmake_version))
        self.ac.add("project({} VERSION {})".format(self.ac.proj_name, self.ac.version))
        #self.ac.add("set(CMAKE_CXX_STANDARD 11)")
        #self.ac.add('set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")\n')

        # Set headers and sources
        self.ac.add("add_library({}".format(self.ac.proj_name))
        self.ac.add("    SHARED")
        for source in self.ac.sources:
            self.ac.add('    "{}"'.format(self.ac.get_posix_path(source)))
        for headers in self.ac.headers:
            self.ac.add('    "{}"'.format(self.ac.get_posix_path(headers)))
        self.ac.add(")\n")

        # Adding the executable
        #self.ac.add("add_executable({} {})\n".format(self.ac.proj_name, r"${SOURCES}"))

        # Setting flags
        self.ac.add("target_compile_definitions({} PUBLIC".format(self.ac.proj_name))
        for flag in self.flags:
           self.ac.add('    "{}"'.format(flag))
        self.ac.add(")\n")

        # Setting executable properties
        #self.ac.add('target_compile_definitions({} PUBLIC OC_MODE_TEST)'.format(self.ac.proj_name))
        #self.ac.add('set_target_properties({} PROPERTIES COMPILE_FLAGS "-fPIC")\n'.format(self.ac.proj_name))

        # Adding include directories
        for include in self.ac.includes:
            if include not in self.ac.library_paths:
                self.ac.add('target_include_directories({} PUBLIC "{}")'.format(self.ac.proj_name, include))
        self.ac.add("")

        # Adding include directories
        for path in self.ac.library_paths:
            self.ac.add('target_include_directories({} PUBLIC "{}")'.format(self.ac.proj_name, path))
        self.ac.add("")

        self.ac.add("find_library(".format(self.ac.proj_name))
        self.ac.add("    log-lib")
        self.ac.add("    log")
        self.ac.add(")\n")

        self.ac.add("target_link_libraries(")
        self.ac.add("    {}".format(self.ac.proj_name))
        self.ac.add(r"    ${log-lib}")
        self.ac.add(")\n")

        # Writing main CMakeLists.txt
        cmake_build_path = self.ac.get_posix_path(os.path.join(self.ac.proj_dir, os.pardir, os.pardir))
        if not os.path.exists(cmake_build_path):
            os.makedirs(cmake_build_path)
        self.ac.write(cmake_build_path)