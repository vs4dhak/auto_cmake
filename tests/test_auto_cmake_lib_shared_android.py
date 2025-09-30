import os
import unittest

from auto_cmake.auto_cmake_android import AutoCMakeLibSharedAndroid

# Source paths
proj_dir = os.path.abspath(os.path.join(os.getcwd(), "resources", "sample_c_proj"))
build_dir = os.path.abspath(os.path.join(os.getcwd(), "resources", "sample_android_proj", "sample_lib_shared_android", "src", "main", "cpp"))

# Configuration
cmake_config = dict()
cmake_config['proj_name'] = 'sample_lib_shared_android'
cmake_config['proj_dir'] = proj_dir
cmake_config['version'] = "2024.03.08"
cmake_config['cmake_version'] = '3.22.1'
cmake_config['include_dirs'] = [proj_dir, build_dir]
cmake_config['libs'] = []
cmake_config['flags'] = ["FLAG_DEMO"]
cmake_config['exclude_dirs'] = ['test', 'cmake-build-debug', 'build']
cmake_config['exclude_paths'] = []
cmake_config['build_dir'] = build_dir

class TestAutoCMakeLibStaticIos(unittest.TestCase):

    def test_build_lib_shared_android(self):
        ac = AutoCMakeLibSharedAndroid(**cmake_config)
        ac.run()

if __name__ == '__main__':
    unittest.main()
