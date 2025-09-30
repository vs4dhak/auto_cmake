#!/usr/bin/env python

"""
Description: Generates a macosx shared library
"""

__author__ = "Veda Sadhak"
__license__ = "MIT"

import os.path

from pbxproj import XcodeProject
from pbxproj.pbxextensions import FileOptions

from .auto_cmake import AutoCMake

class AutoCMakeLibStaticIos():

    def __init__(self, **cmake_config):

        # Creating instance
        self.ac = AutoCMake(**cmake_config)

        # Public headers
        if "public_headers" in cmake_config.keys():
            self.public_headers = cmake_config["public_headers"]

        # XCode proj path
        if "xcode_proj" in cmake_config.keys():
            self.xcode_proj = self.ac.get_posix_path(cmake_config["xcode_proj"])
        else:
            raise ("cmake_config['xcode_proj'] must be specified (e.g. an empty XCode Static Lib project")

    def xcode_add_flags(self):

        # Load XCode project
        project = XcodeProject.load(self.xcode_proj)

        for target in project.objects.get_targets():
            for flag in self.ac.flags:
                project.add_flags('OTHER_CFLAGS', f"-D{flag}", target.name)

        project.save()

    def xcode_rmv_flags(self):

        # Load XCode project
        project = XcodeProject.load(self.xcode_proj)

        for target in project.objects.get_targets():
            for flag in self.ac.flags:
                project.remove_flags('OTHER_CFLAGS', f"-D{flag}", target.name)

        project.save()

    def xcode_find_file(self, project, file_path):
        file_name = os.path.basename(file_path)
        # Iterate over all PBXFileReference objects in the project
        for obj in project.objects.get_objects_in_section('PBXFileReference'):
            # Access the 'name' and 'path' attributes directly, with a fallback
            obj_name = obj.name if 'name' in obj else None
            obj_path = obj.path if 'path' in obj else None

            # Now compare using these variables
            if file_name == obj_name or file_name == obj_path.split('/')[-1]:
                return obj
        return None

    def xcode_rmv_header(self, project, header):
        for target in project.objects.get_targets():
            file = self.xcode_find_file(project, header)
            if file:
                for config in project.objects[target.buildConfigurationList].buildConfigurations:
                    # Each config is a reference to a PBXBuildConfiguration object
                    # You can access its buildSettings dictionary directly
                    build_settings = project.objects[config].buildSettings
                    if 'LIBRARY_SEARCH_PATHS' in build_settings:
                        library_search_paths = build_settings['LIBRARY_SEARCH_PATHS']

                        if header in library_search_paths:
                            library_search_paths.remove(header)
                            build_settings['LIBRARY_SEARCH_PATHS'] = library_search_paths

                        dir = os.path.dirname(file.path)
                        if type(library_search_paths) == list:
                            for path in library_search_paths:
                                if dir in path:
                                    library_search_paths.remove(path)
                                    build_settings['LIBRARY_SEARCH_PATHS'] = library_search_paths
                        elif type(library_search_paths) == str:
                            if dir in library_search_paths:
                                build_settings['LIBRARY_SEARCH_PATHS'] = ''

                # Update header search paths
                project.remove_header_search_paths(header, target_name=target.name)
                project.remove_header_search_paths(file.path, target_name=target.name)

                # Remove file
                project.remove_file_by_id(file.get_id())

    def xcode_add_headers(self):

        # Load XCode project
        project = XcodeProject.load(self.xcode_proj)

        group_headers = project.get_or_create_group('headers')

        # Add header paths to all targets in the project
        for header in self.ac.headers:
            project.add_header_search_paths([header], recursive=False)
            file_options = FileOptions(header_scope='Public')
            project.add_file(header, parent=group_headers, tree='SOURCE_ROOT', file_options=file_options, force=False)

        # Save the project file
        project.save()

    def xcode_add_sources(self):

        # Load XCode project
        project = XcodeProject.load(self.xcode_proj)

        group_sources = project.get_or_create_group('sources')

        # Add header paths to all targets in the project
        for source in self.ac.sources:
            project.add_file(source, parent=group_sources, tree='SOURCE_ROOT', force=False)

        # Save the project file
        project.save()

    def xcode_rmv_headers(self):

        # Load XCode project
        project = XcodeProject.load(self.xcode_proj)

        # Add header paths to all targets in the project
        for header in self.ac.headers:
            self.xcode_rmv_header(project, header)

        # Save the project file
        project.save()

    def xcode_rmv_sources(self):

        # Load XCode project
        project = XcodeProject.load(self.xcode_proj)

        # Add header paths to all targets in the project
        for source in self.ac.sources:
            file = self.xcode_find_file(project, source)
            if file:
                project.remove_file_by_id(file.get_id())

        # Save the project file
        project.save()

    def run(self):

        self.ac.index()
        self.xcode_add_flags()
        self.xcode_add_headers()
        self.xcode_add_sources()
