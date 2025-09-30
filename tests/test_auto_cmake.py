import os
import json
import unittest

from auto_cmake.auto_cmake import AutoCMake
from auto_cmake.auto_cmake_exe import AutoCMakeExe

# Source paths
proj_dir = os.path.abspath(os.path.join(os.getcwd(), "resources", "sample_c_proj"))
build_dir = os.path.abspath(os.path.join(proj_dir, "build"))

# Configuration
cmake_config = dict()
cmake_config['proj_name'] = 'sample_c_proj'
cmake_config['proj_dir'] = proj_dir
cmake_config['version'] = "2024.03.08"
cmake_config['cmake_version'] = '3.15'
cmake_config['include_dirs'] = [proj_dir]
cmake_config['libs'] = []
cmake_config['flags'] = ["FLAG_DEMO"]
cmake_config['exclude_dirs'] = []
cmake_config['exclude_paths'] = []
cmake_config['build_dir'] = build_dir

class TestAutoCMakeExe(unittest.TestCase):

    def test_create_build_dir(self):
        ac = AutoCMake(**cmake_config)
        ac.create_build_dir()

        build_dir = ac.get_posix_path(cmake_config['build_dir'])
        self.assertTrue(os.path.exists(build_dir))

    def test_export(self):
        ac = AutoCMake(**cmake_config)
        ac.index()
        ac.export()

        include_dir = ac.get_posix_path(os.path.join(cmake_config['build_dir'], "include"))
        src_dir = ac.get_posix_path(os.path.join(cmake_config['build_dir'], "src"))
        self.assertTrue(os.path.exists(include_dir))
        self.assertTrue(os.path.exists(src_dir))

if __name__ == '__main__':
    unittest.main()
