<h2> Auto CMake </h2>

Automate setup of CMake projects for large C & C++ projects on all platforms: Windows, MacOS, Linux, Android, iOS and Bare-Metal<br>
- Automatically indexes .c, .h, .cpp, .hpp files and creates entries in CMakeLists.txt
- Automatically generates CMakeLists.txt for subdirectories and create library entries in CMakeLists.txt
- Automatically configures XCode projects with header, source and library paths
- Automatically configures Android projects with header, source and library paths

<h2> Contents </h2>

```
1) auto_cmake......................Source
   1.1) resources..................CMake Toolchain Files
2) scripts ........................Deployment Scripts
3) tests...........................Unit Tests for Windows, MacOS, Linux, Android, iOS and Bare-Metal
   3.1) resources .................Sample
      3.1.1) sample_c_proj.........Generic Project to Validate Compilation on PC via Unit Tests
      3.1.2) sample_android_proj...Project to Validate Compilation on Android via Unit Tests
      3.1.3) sample_xcode_proj.....Project to Validate Compilation on iOS via Unit Tests
```

<h2> Sample Usage </h2>

Steps:

1) Download auto-cmake from: https://pypi.org/project/auto-cmake/
2) In your project define a auto cmake script (sample below)
3) This file defines (among other things):
   1) The project name and version
   2) Directories and paths to include and exclude
   3) Compiler flags
   4) Build directory
4) Run the script to generate the CMake project
   
```
import os
import unittest

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

ac = AutoCMakeExe(**cmake_config)
ac.run()
```