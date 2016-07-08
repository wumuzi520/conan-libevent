[![Build Status](https://travis-ci.org/theirix/conan-libevent.svg)](https://travis-ci.org/theirix/conan-libevent)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/theirix/conan-lbevent)](https://ci.appveyor.com/project/theirix/conan-libevent)


# conan-libevent

[Conan.io](https://conan.io) package for [libevent](https://github.com/libevent/libevent) library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/libevent/2.0.22/theirix/stable).

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload libevent/2.0.22@theirix/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install libevent/2.0.22@theirix/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    libevent/2.0.22@theirix/stable

    [options]
    libevent:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
