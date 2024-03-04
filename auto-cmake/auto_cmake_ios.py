#!/usr/bin/env python

"""
Description: Generates a macosx shared library
"""

__author__ = "Veda Sadhak"
__license__ = "MIT"
__version__ = "2024.03.03"

import os
import shutil

from auto_cmake import AutoCMake

class AutoCMakeIos():

    def __init__(self, **cmake_config):

        # Creating instance
        self.ac = AutoCMake(**cmake_config)
        self.libs = cmake_config["libs"]

        # Setting flags
        self.flags = cmake_config["flags"]

        # Public headers
        self.public_headers = cmake_config["public_headers"]

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
        self.ac.add('set(CMAKE_SUPPRESS_REGENERATION true)\n')
        # self.ac.add('set(CMAKE_OSX_ARCHITECTURES arm64)\n')
        self.ac.add('set(CMAKE_SYSTEM_NAME SIMULATOR64)\n')
        self.ac.add('set(CMAKE_SYSTEM_VERSION 16.4)\n')
        # self.ac.add('set(CMAKE_OSX_SYSROOT "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator16.4.sdk")\n')

        # Setting flags
        self.ac.add('SET_PROPERTY(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS TRUE)\n')

        # Set sources
        self.ac.add("set(SOURCES".format(self.ac.proj_name))
        for source in self.ac.sources:
            self.ac.add('    "{}"'.format(self.ac.get_posix_path(source)))
        self.ac.add(")\n")

        # Add headers
        self.ac.add('set(HEADERS')
        for header in self.ac.headers:
            self.ac.add('    "{}"'.format(header))
        self.ac.add(")")

        # Adding the shared lib
        self.ac.add(f"add_library({self.ac.proj_name} SHARED")
        self.ac.add(r"    ${SOURCES}")
        self.ac.add(r"    ${HEADERS}")
        self.ac.add(")\n")

        # Add headers
        self.ac.add('set(INCLUDES')
        for include in self.ac.includes:
            self.ac.add('    "{}"'.format(include))
        self.ac.add(")")
        self.ac.add('include_directories(${INCLUDES})\n')

        # Add headers
        self.ac.add('set(PUBLIC_HEADERS')
        for header in self.ac.headers:
            #for public_header in self.public_headers:
            #    if public_header in header:
                    self.ac.add('    "{}"'.format(header))
        self.ac.add(")")

        # Set target properties
        self.ac.add(f"set_target_properties({self.ac.proj_name}")
        self.ac.add(f"    PROPERTIES")
        self.ac.add(f"    FRAMEWORK TRUE")
        self.ac.add(f"    FRAMEWORK_VERSION C")
        self.ac.add(f"    MACOSX_FRAMEWORK_IDENTIFIER {self.ac.proj_name}")
        self.ac.add( "    MACOSX_FRAMEWORK_INFO_PLIST ${PROJECT_SOURCE_DIR}/../platform/ios/Info.plist")
        self.ac.add(f"    VERSION 16.4.0")
        self.ac.add(f"    SOVERSION 1.0.0")
        self.ac.add(f'    XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY "iPhone Developer"')
        self.ac.add( '    PUBLIC_HEADER ${PUBLIC_HEADERS}')
        self.ac.add(")\n")

        # for header in self.ac.headers:
        #     for public_header in self.public_headers:
        #         if public_header in header:
        #             self.ac.add(f"install(FILES {header} DESTINATION include)")
        # self.ac.add("\n")

        # Setting flags
        self.ac.add("target_compile_definitions({} PUBLIC".format(self.ac.proj_name))
        for flag in self.flags:
            self.ac.add('    "{}"'.format(flag))
        self.ac.add(")\n")

        # Link libraries
        for lib in self.libs:
            self.ac.add('target_link_libraries({} {})\n'.format(self.ac.proj_name, self.ac.get_posix_path(lib)))

        # Adding headers
        for include in self.ac.includes:
            if include not in self.ac.library_paths:
                self.ac.add('target_include_directories({} PUBLIC "{}")'.format(self.ac.proj_name, include))
        self.ac.add("")

        # Adding libraries
        for path in self.ac.library_paths:
            self.ac.add('target_include_directories({} PUBLIC "{}")'.format(self.ac.proj_name, path))
        self.ac.add("")

        # Writing main CMakeLists.txt
        cmake_build_path = self.ac.get_posix_path(os.path.join(self.ac.proj_dir, "build"))
        if not os.path.exists(cmake_build_path):
            os.makedirs(cmake_build_path)
        self.ac.write(cmake_build_path)

        # Copy over headers
        xcode_file = f"{self.ac.proj_name}.framework"
        dst = os.path.join(cmake_build_path, "Debug", xcode_file, "Headers")
        if not os.path.exists(dst):
            os.makedirs(dst)
        for header in self.ac.headers:
            header_path, header_file = os.path.split(header)
            shutil.copyfile(header, os.path.join(dst, header_file))

        # Copy over Info.plist
        src = os.path.join(self.ac.proj_dir, "platform", "ios", "Info.plist")
        dst = os.path.join(cmake_build_path, "Debug", xcode_file, "Info.plist")
        shutil.copyfile(src, dst)

        # xcode_file = f"{self.ac.proj_name}.xcodeproj"
        # src = self.ac.get_posix_path(os.path.join(self.ac.proj_dir, "platform", "ios", xcode_file))
        # dst = os.path.join(cmake_build_path, xcode_file)
        # if os.path.exists(dst):
        #     shutil.rmtree(dst)
        # shutil.copytree(src, dst)
        # print("Copied xcode config")

        # Copy .cmake file
        src_file = self.ac.get_posix_path(os.path.join(self.ac.proj_dir, "Scripts", "cmake", "auto_cmake", "resources", "ios.toolchain.cmake"))
        dst_file = self.ac.get_posix_path(os.path.join(self.ac.proj_dir, "build", "ios.toolchain.cmake"))
        shutil.copyfile(src_file, dst_file)


