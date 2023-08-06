Brandon the Devpi Builder
=========================
[![Build Status](https://travis-ci.org/blue-yonder/devpi-builder.svg?branch=master)](https://travis-ci.org/blue-yonder/devpi-builder)
[![Coverage Status](https://coveralls.io/repos/blue-yonder/devpi-builder/badge.png?branch=master)](https://coveralls.io/r/blue-yonder/devpi-builder?branch=master)
[![Latest Version](https://pypip.in/version/devpi-builder/badge.svg)](https://pypi.python.org/pypi/devpi-builder/)
[![Requirements Status](https://requires.io/github/blue-yonder/devpi-builder/requirements.png?branch=master)](https://requires.io/github/blue-yonder/devpi-builder/requirements/?branch=master)

Brandon, the devpi-builder, takes a `requirements.txt` and incrementally fills a [devpi](http://doc.devpi.net/latest/) index with wheels of the listed python packages.


Brandon by Example:
-------------------

Given a `requirements.txt`, we can upload all listed packages to the index `opensource/Debian_7` using the following command:

    $ devpi-builder requirements.txt opensource/Debian_7 opensource mypassword
    
Example of such a requirements.txt:

    progressbar==0.2.2 
    progressbar==0.2.1 
    PyYAML==3.11

Commandline Usage
-----------------

    usage: devpi-builder [-h] [--blacklist BLACKLIST] [--pure-index PURE_INDEX]
                         [--junit-xml JUNIT_XML]
                         requirements index user password
    
    Create wheels for all given project versions and upload them to the given
    index.
    
    positional arguments:
      requirements          requirements.txt style file specifying which project
                            versions to package.
      index                 The index to upload the packaged software to.
      user                  The user to log in as.
      password              Password of the user.
    
    optional arguments:
      -h, --help            show this help message and exit
      --blacklist BLACKLIST
                            Packages matched by this requirements.txt style file
                            will never be build.
      --pure-index PURE_INDEX
                            The index to use for pure packages. Any non-pure
                            package will be uploaded to the index given as
                            positional argument. Packages already found in the pure
                            index will not be built, either.
      --junit-xml JUNIT_XML
                            Write information about the build success / failure to
                            a JUnit-compatible XML file.

Features & Backlog
------------------

 * [x] Read a `requirements.txt` stile input file.
 * [x] Support multiple versions of a package in the same file 
 * [x] Only build packages not yet in the target index.
 * [x] Support a black-list for packages to never be built and uploaded (certain packages like numpy are fragile regarding their interdependency with other packages).
 * [ ] Support extras requirements of packages
 * [x] Can use separate indices for plain python packages and those with binary contents.
 * [x] Can log build results to a JUnit compatible XML file, thus that it can be parsed by Jenkins.


License
-------

[New BSD](COPYING)
