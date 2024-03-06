#!/usr/bin/env python

"""
Description: Generates an executable target
"""

__author__ = "Veda Sadhak"
__license__ = "MIT"

import os
import shutil

from .auto_cmake import AutoCMake

class AutoCMakeSTM32():

    def __init__(self, **cmake_config):

        # Creating instance
        self.ac = AutoCMake(**cmake_config)

        # Setting flags
        self.linker_file = cmake_config["linker_file"]
        self.c_flags = cmake_config["c_flags"]
        self.cxx_flags = cmake_config["cxx_flags"]

        self.compile_options = ""
        for option in cmake_config["compile_options"]:
            self.compile_options += option + " "

        self.link_options = ""
        for option in cmake_config["link_options"]:
            self.link_options += option + " "

        self.definitions = ""
        for definition in cmake_config["definitions"]:
            self.definitions += definition + " "

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

        # Set headers and sources
        self.ac.add("set(SOURCES".format(self.ac.proj_name))
        for source in self.ac.sources:
            self.ac.add('    "{}"'.format(self.ac.get_posix_path(source)))
        for headers in self.ac.headers:
            self.ac.add('    "{}"'.format(self.ac.get_posix_path(headers)))
        self.ac.add(")\n")

        # Adding the startup file
        if (len(self.ac.startup) != 1):
            raise Exception(f"Invalid number of startup files: {len(self.ac.startup)}")
        else:
            startup_file = self.ac.startup[0]
            self.ac.add(f'add_library(STARTUP "{startup_file}")')
            self.ac.add(f'set_source_files_properties("{startup_file}" PROPERTIES COMPILE_FLAGS "-x assembler-with-cpp")')
            self.ac.add(f'set_property(SOURCE "{startup_file}" PROPERTY LANGUAGE C)')
            self.ac.add("")

        # Add the compiler
        self.ac.add("set(CMAKE_C_COMPILER arm-none-eabi-gcc)")
        self.ac.add("set(CMAKE_CXX_COMPILER arm-none-eabi-g++)")
        self.ac.add("set(OBJCOPY arm-none-eabi-objcopy)")
        self.ac.add("")

        # Find linker path
        if not self.linker_file:
            raise Exception(f"No linker specified.")
        elif len(self.ac.linkers) == 0:
            raise Exception(f"No linkers found.")
        else:
            for linker_path in self.ac.linkers:
                if self.linker_file in linker_path:
                    self.linker_path = linker_path

        # Setup linker
        self.ac.add(f'set(COMMON_FLAGS "{self.compile_options}")')
        self.ac.add(f'set(CMAKE_C_FLAGS "{self.compile_options} {self.c_flags}")')
        self.ac.add(f'set(CMAKE_CXX_FLAGS "{self.compile_options} {self.cxx_flags}")')
        self.ac.add(f'set(CMAKE_EXE_LINKER_FLAGS "{self.link_options} -T {self.linker_path}")')
        self.ac.add("")

        # Adding the executable
        self.ac.add("add_executable({}.elf {} {})\n".format(self.ac.proj_name, r"${SOURCES}", r"${LINKER_SCRIPT}"))
        self.ac.add("")

        # Adding include directories
        for path in self.ac.library_paths:
            self.ac.add('target_include_directories({}.elf PUBLIC "{}")'.format(self.ac.proj_name, path))
        self.ac.add("")

        # Setting flags
        self.ac.add(f'target_compile_definitions({self.ac.proj_name}.elf PRIVATE {self.definitions})')
        self.ac.add("")

        # Setup build files
        self.ac.add('target_link_libraries(${PROJECT_NAME}.elf STARTUP)')
        self.ac.add('set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-gc-sections,--print-memory-usage,-Map=${PROJECT_NAME}.map")')
        self.ac.add('set(HEX_FILE ${PROJECT_SOURCE_DIR}/${PROJECT_NAME}.hex)')
        self.ac.add('set(BIN_FILE ${PROJECT_SOURCE_DIR}/${PROJECT_NAME}.bin)')
        self.ac.add("")

        # Setup build command
        self.ac.add(r'add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD')
        self.ac.add(r'                   COMMAND ${OBJCOPY} -Oihex ${PROJECT_NAME}.elf ${HEX_FILE}')
        self.ac.add(r'                   COMMAND ${OBJCOPY} -Obinary ${PROJECT_NAME}.elf ${BIN_FILE}')
        self.ac.add(r'                   COMMENT "Building ${HEX_FILE} \nBuilding ${BIN_FILE}"')
        self.ac.add(r'                   COMMAND arm-none-eabi-size ${PROJECT_NAME}.elf)')
        self.ac.add("")

        # Writing main CMakeLists.txt
        self.ac.create_build_dir()
        self.ac.write(self.ac.build_dir)

        # Copy toolchain file
        src_file = self.ac.get_posix_path(os.path.join(self.ac.proj_dir, "Scripts", "cmake", "auto_cmake", "resources", "arm-none-eabi-gcc.toolchain.cmake"))
        dst_file = self.ac.get_posix_path(os.path.join(self.ac.proj_dir, "cmake-build-debug", "arm-none-eabi-gcc.toolchain.cmake"))
        shutil.copyfile(src_file, dst_file)