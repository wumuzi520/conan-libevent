[ ![Download](https://api.bintray.com/packages/bincrafters/public-conan/libevent%3Abincrafters/images/download.svg?version=2.0.22%3Astable) ](https://bintray.com/bincrafters/public-conan/libevent%3Abincrafters/2.0.22%3Astable/link)
[![Build Status](https://travis-ci.org/bincrafters/conan-libevent.svg?branch=stable%2F2.0.22)](https://travis-ci.org/bincrafters/conan-libevent)
[![Build status](https://ci.appveyor.com/api/projects/status/yxj9deyub8b7p34c/branch/stable/2.0.22?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-libevent/branch/stable/2.0.22)

## This repository holds a conan recipe for libevent.

[Conan.io](https://conan.io) package for [libevent](http://libevent.org/) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/libevent%3Abincrafters).

## For Users: Use this package

### Basic setup

    $ conan install libevent/2.0.22@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    libevent/2.0.22@bincrafters/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..
	
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git. 

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Build  and package 

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method. 

    $ conan create bincrafters/stable
	
## Add Remote

	$ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload libevent/2.0.22@bincrafters/stable --all -r bincrafters

### License
[3-Clause BSD](http://libevent.org/LICENSE.txt)
