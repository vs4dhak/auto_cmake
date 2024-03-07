<h2> Auto CMake: </h2>

Automate setup of CMake projects for large C & C++ projects on all platforms: Windows, MacOS, Linux, Android, iOS and Bare-Metal<br>
- Automatically indexes .c, .h, .cpp, .hpp files and creates entries in CMakeLists.txt
- Automatically generates CMakeLists.txt for subdirectories and create library entries in CMakeLists.txt
- Automatically configures XCode projects with header, source and library paths
- Automatically configures Android projects with header, source and library paths

<h2> Contents: </h2>

```
1) auto_cmake......................Source
   1.1) resources..................CMake Toolchain Files
2) scripts ........................Deployment Scripts
3) tests...........................Unit Tests for Windows, MacOS, Linux, Android, iOS and Bare-Metal
   3.1) resources .................Sample
      3.1.1) sample_xcode_proj.....Generic Project to Validate Compilation on PC via Unit Tests
      3.1.2) sample_android_proj...Project to Validate Compilation on Android via Unit Tests
      3.1.3) sample_xcode_proj.....Project to Validate Compilation on iOS via Unit Tests
```

<h2> Sample Usage: </h2>

Steps:

1) Create a python script that will import AutoCMake
2) In this file define
   1) The project name and version
   2) Directories and paths to include and exclude
   3) Compiler flags
   4) Build directory
   
```
import os

from .auto_cmake_exe import AutoCMakeExe

# Configuration
cmake_config = dict()
cmake_config['proj_name'] = 'proj_name'
cmake_config['proj_dir'] = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
cmake_config['version'] = '0.01'
cmake_config['cmake_version'] = '3.15'
cmake_config['exclude_folders'] = ['excluded-folder-1', 'excluded-folder-2']

# Generate CMake
cme = AutoCMakeExe(**cmake_config)
cme.run()
```

3) Run the script to generate all the CMakeLists.txt files