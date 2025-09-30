#!/usr/bin/env python

"""
Description: Core module.
"""

__author__ = "Veda Sadhak"
__license__ = "MIT"

import os
import pathlib
import shutil
from .auto_cmake_indexer import AutoCMakeIndexer

class AutoCMake(AutoCMakeIndexer):

    def __init__(self, **kwargs):

        AutoCMakeIndexer.__init__(self, kwargs['proj_dir'])

        # Project Definition
        self.proj_name = kwargs['proj_name']
        self.version = kwargs['version']

        # CMake Definition
        self.cmake_version = kwargs['cmake_version']

        # Setting flags
        self.flags = kwargs["flags"]

        # Build & Export
        self.build_dir = self.get_posix_path(kwargs['build_dir'])

        # Include & Excludes
        self.include_dirs = kwargs['include_dirs']
        self.exclude_dirs = kwargs['exclude_dirs']
        self.exclude_paths = kwargs['exclude_paths']

        # Internal excludes
        self.exclude_paths.append(self.build_dir)

        # Library cache
        self.library_paths = []
        self.library_names = []

        # File cache
        self.sources = []
        self.headers = []
        self.includes = []
        self.startup = []
        self.linkers = []

    def clear(self):

        self.acake = ''

    def add(self, line):
        self.acake += (line + "\n")

    def write(self, path):

        with open(os.path.join(path, "CMakeLists.txt"), "w") as file:
            file.write(self.acake)

    def get_posix_path(self, path):

        return str(pathlib.PureWindowsPath(path).as_posix())

    def check_for_extensions(self, files, extensions):

        for file in files:
            for extension in extensions:
                if extension in file[-len(extension):]:
                    return True
        return False

    def construct_lib(self, lib_path, lib_name, lib_files):

        self.clear()
        self.add("add_library(")
        self.add("   " + lib_name)
        for lib_file in lib_files:

            # Check for exclusion
            is_excluded = False
            for exclude_path in self.exclude_paths:
                full_path = lib_path+"/"+lib_file
                if full_path[-len(exclude_path):] in exclude_path:
                    is_excluded = True
                    break

            # Add library
            if not is_excluded:
                if (not "CMakeLists" in lib_file):
                    self.add("    " + lib_file)
                if (".cpp" in lib_file) or (".c" in lib_file):
                    self.sources.append(os.path.join(lib_path,lib_file))

        self.add(")\n")
        self.add('target_include_directories({} PUBLIC "{}")'.format(lib_name, lib_path))
        self.write(lib_path)

        print("Added library {}".format(lib_name))

    def add_library(self, path):

        files = self.get_files(path)
        contains_source = self.check_for_extensions(files, [".c", ".cpp"])
        contains_header = self.check_for_extensions(files, [".h", ".hpp"])
        contains_startup = self.check_for_extensions(files, [".s"])
        contains_linker = self.check_for_extensions(files, [".ld"])

        if (len(files) > 0) and (contains_source):

            # Getting the library name while checking for repeats
            raw_lib_name = os.path.basename(path)
            lib_name_index = 1
            lib_name = raw_lib_name
            while (lib_name in self.library_names):
                lib_name = raw_lib_name + "_{}".format(lib_name_index)
                lib_name_index+=1

            # Constructing lib path
            lib_path = self.get_posix_path(path)

            # Adding the library
            if (lib_path not in self.library_paths) and (lib_name not in self.library_names):
                self.library_paths.append(lib_path)
                self.library_names.append(lib_name)
                self.construct_lib(lib_path, lib_name, files)

        if (len(files) > 0) and (contains_header):

            # Getting the library name while checking for repeats
            raw_lib_name = os.path.basename(path)
            lib_name_index = 1
            lib_name = raw_lib_name
            while (lib_name in self.library_names):
                lib_name = raw_lib_name + "_{}".format(lib_name_index)
                lib_name_index+=1

            # Constructing lib path
            lib_path = self.get_posix_path(path)

            # Adding the library
            if (lib_path not in self.library_paths) and (lib_name not in self.library_names):
                self.library_paths.append(lib_path)
                self.library_names.append(lib_name)
                self.construct_lib(lib_path, lib_name, [])

            # Adding include dirs
            self.includes.append(self.get_posix_path(path))

            # Adding the headers
            for file in files:

                # Check for exclusion
                is_excluded = False
                full_path = self.get_posix_path(os.path.join(path, file))
                for exclude_path in self.exclude_paths:
                    if full_path[-len(exclude_path):] in exclude_path:
                        is_excluded = True

                if not is_excluded:
                    if (".hpp" in file) or (".h" in file):
                        self.headers.append(full_path)

        if (len(files) > 0) and (contains_startup):

            # Adding include dirs
            self.includes.append(self.get_posix_path(path))

            # Adding the headers
            for file in files:
                if (".s" in file):
                    self.startup.append(self.get_posix_path(os.path.join(path, file)))

        if (len(files) > 0) and (contains_linker):

            # Adding include dirs
            self.includes.append(self.get_posix_path(path))

            # Adding the headers
            for file in files:
                if (".ld" in file):
                    self.linkers.append(self.get_posix_path(os.path.join(path, file)))

    def add_libraries(self, path):

        if (self.sub_dirs_exist(path)):
            for dir in self.get_sub_dirs(path):

                lib_path = os.path.join(path,dir)

                excluded = False
                for exclude_dir in self.exclude_dirs:
                    if exclude_dir == dir:
                        excluded = True

                if not excluded:
                    for exclude_path in self.exclude_paths:
                        if self.get_posix_path(exclude_path) in self.get_posix_path(lib_path):
                            excluded = True

                if not excluded:
                    self.add_libraries(os.path.join(path,dir))

        self.add_library(path)

    def index(self):

        for _dir in self.include_dirs:
            self.add_libraries(os.path.join(self.proj_dir, _dir))
            self.clear()

    def create_build_dir(self):
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)

    def export(self):

        # Create directories
        include_dir = self.get_posix_path(os.path.join(self.build_dir, "include"))
        src_dir = self.get_posix_path(os.path.join(self.build_dir, "src"))
        if not os.path.exists(include_dir):
            os.makedirs(include_dir)
        if not os.path.exists(src_dir):
            os.makedirs(src_dir)

        # Copy over headers
        for header in self.headers:
            header_path, header_file = os.path.split(header)
            shutil.copyfile(header, os.path.join(include_dir, header_file))

        # Copy over sources
        for source in self.sources:
            source_path, source_file = os.path.split(source)
            shutil.copyfile(source, os.path.join(src_dir, source_file))




