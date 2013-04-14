goxgui
======

About
-----

goxgui is a Qt front end for [prof7bit's goxtool](http://prof7bit.github.io/goxtool/). This is what it looks like:

![Screenshot](https://raw.github.com/sebastianhaberey/goxgui/master/screenshot.png)

Features
--------

* Display asks / bids
* Display MtGox account balance (USD/BTC)
* Display MtGox lag
* Place and cancel orders (USD)

Prerequisites
-------------

I have tested the application on **OSX 10.7.5** and **Windows XP** within the following confguration. Other setups may or may not work.

* Python 2.7.3
* Qt 4.8.2
* PyQt (matching the above Python / Qt versions)
* pycrypto 2.6

goxtool will be installed with goxgui, so you don't need to install it manually.

Installation
------------

Please note: **you must make sure all prerequisites are installed**, otherwise the application will not work.

    git clone --recursive git://github.com/sebastianhaberey/goxgui.git
    cd goxgui/run
    chmod 755 ./start.sh
    ./start.sh

Requests
--------

Bugs and feature requests can be posted in [the goxgui thread on bitcointalk.org](https://bitcointalk.org/index.php?topic=176489.0).

Disclaimer
----------

This software is provided “as is," and you use the software at your own risk. 
