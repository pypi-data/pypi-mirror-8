Quick Start
***********

Installation
============

::

    pip install pingme

Android app available on the app store.

Configuration
=============

Configuration can be put into ~/.pingme_config or specified on the command line.

::

    pingme -d <device-id> <message>

Configuration file should look like this ::

    [Default]
    devices=<devices>
    message=<message>

Command line arguments will override the configuration file.
