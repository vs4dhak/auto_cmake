import os
import unittest

from auto_cmake.auto_cmake_ios import AutoCMakeLibStaticIos

# Source paths
proj_dir = os.path.abspath(os.path.join(os.getcwd(), "resources", "sample_c_proj"))
xcode_proj_dir = os.path.abspath(os.path.join(os.getcwd(), "resources", "sample_xcode_proj", "sample_xcode_proj.xcodeproj", "project.pbxproj"))
build_dir = os.path.abspath(os.path.join(proj_dir, "build", "build_ios"))

# Configuration
cmake_config = dict()
cmake_config['proj_name'] = 'sample_c_proj'
cmake_config['proj_dir'] = proj_dir
cmake_config['version'] = "2024.03.08"
cmake_config['cmake_version'] = '3.15'
cmake_config['include_dirs'] = [proj_dir]
cmake_config['libs'] = []
cmake_config['flags'] = ["FLAG_DEMO"]
cmake_config['exclude_dirs'] = ['test']
cmake_config['exclude_paths'] = []
cmake_config['build_dir'] = build_dir
cmake_config['xcode_proj'] = xcode_proj_dir

class TestAutoCMakeLibStaticIos(unittest.TestCase):

    def test_add_to_xcode(self):
        ac = AutoCMakeLibStaticIos(**cmake_config)
        ac.run()

    def test_rmv_from_xcode(self):
        ac = AutoCMakeLibStaticIos(**cmake_config)
        ac.ac.index()
        ac.xcode_rmv_flags()
        ac.xcode_rmv_headers()
        ac.xcode_rmv_sources()

if __name__ == '__main__':
    unittest.main()
