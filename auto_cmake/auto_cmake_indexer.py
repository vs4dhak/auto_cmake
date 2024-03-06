#!/usr/bin/env python

"""
Description: Builds a source index.
"""

__author__ = "Veda Sadhak"
__license__ = "MIT"

import os

class AutoCMakeIndexer():

    def __init__(self, proj_dir):

        # Getting the project dir
        self.proj_dir = proj_dir

        # Directory indices
        self.all_dirs = []
        self.include_dirs = []

        # File indices
        self.files = dict()

    def get_sub_dirs(self, path):
        return next(os.walk(path))[1]

    def sub_dirs_exist(self, path):
        return (len(next(os.walk(path))[1]) > 0)

    def index_dirs(self, path):

        if (self.sub_dirs_exist(path)):
            for dir in self.get_sub_dirs(path):
                self.index_dirs(os.path.join(path, dir))

        self.all_dirs.append(path)

    def get_files(self, path):
        return next(os.walk(path))[2]