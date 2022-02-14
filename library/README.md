# AS7262 Spectral Sensor

[![Build Status](https://travis-ci.com/pimoroni/as7262-python.svg?branch=master)](https://travis-ci.com/pimoroni/as7262-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/as7262-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/as7262-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/as7262.svg)](https://pypi.python.org/pypi/as7262)
[![Python Versions](https://img.shields.io/pypi/pyversions/as7262.svg)](https://pypi.python.org/pypi/as7262)

Suitable for detecting the properties of ambient light, light passing through a liquid or light reflected from an object the AS7262 spectral sensor has 6 spectral channels at 450 (violet), 500 (blue), 550 (green), 570 (yellow), 600 (orange) and 650nm (red).

# Installing

Stable library from PyPi:

* Just run `sudo pip install as7262`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/as7262-python`
* `cd as7262-python`
* `sudo ./install.sh`


# Changelog
0.1.0
-----

* Port to new i2cdevice API
* Breaking change from singleton module to AS7262 class

0.0.2
-----

* Extended reset delay to avoid IO Errors

0.0.1
-----

* Initial Release
