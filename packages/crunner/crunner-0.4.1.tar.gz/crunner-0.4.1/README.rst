Crunner
=======

Crunner is small application to run test after every change and notify about results

Main features:

    * Continuously watch directories
    * Execute proper tests after every change
    * Send notification about test result
    * Test framework independent
    * Notifier independent

Requirements
============

    * Python 2.7
    * watchdog
    * mock

Installation
============

::

    pip install crunner

Download
========

Latest version of package is available in `drone.io project artifacts <a href="https://drone.io/github.com/pchomik/crunner/files">`.

Configuration
=============

Configuration file **.crunner.json** has to created in user home directory. The format of the file looks like below:

::

    {
      "main": {
        "run_on_start": true,
        "delay": 5
      },
      "notifier": {
        "cmd": "/usr/bin/notify-send",
        "img_arg": "-i",
        "msg_arg": "",
        "add_args": ""
      },
      "tester": {
        "cmd": "py.test",
        "args": "-s --timeout 1 --pep8"
      },
      "projects": {
        "pytest-crunner": {
          "active": true,
          "test_path": "/home/user/crunner/test/",
          "project_path": "/home/user/crunner",
          "watching_types": [".*.py"]
        }
      }
    }

Presented configuration is notifier and test framework independent. 
It is possible to extend this configuration to watch multiple projects by adding new configuration project.

Execution
=========

The main command is: **crun**

Executed without argument will watch and test all projects configured as active.

Executed with project name argument will watch and test only specified project.

::

    # To watch and test all active projects
    crun

    # To watch and test only one project
    crun some_project

License
=======

crunner - Application to run test after every change and notify about results.

Copyright (C) 2014 Pawel Chomicki

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
