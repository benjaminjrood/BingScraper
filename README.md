# BingScraper #

BingScraper is a Python script that executes Bing queries for the sole purpose of generating Bing Reward points.  Please note that running this script may get your account banned, so tread carefully.  You have been warned!

### How do I get set up? ###

* Install Python version 3
* Clone this repository or directly download BingScraper.py
* Install [Selenium](http://selenium-python.readthedocs.org/installation.html).  The easiest method to do this is via pip or easy_install.
* Install Firefox.
* Once per day, execute: python BingScraper.py <account_username> <password>

### Notes and Caveats ###

* If you have multiple Microsoft accounts, simply execute the script more than once.
* The script run.sh can be modified to run as a cron task, and can also be configured to send a report email after each execution.
* I'm not bothering to support Python 2.X, it's old and I just don't feel like making this any more complex than it needs to be.  If YOU wan to make it support old versions of Python, feel free to do so and submit a pull request. 

### Raspberry Pi Guidelines ###
Additions to the script have been recently added so that it can be run on a Raspberry Pi in headless mode (e.g. no monitor is attached).  To do so, there are a few additional packages that need to be installed:

* Xvfb
* Iceweasel
* Xvfbwrapper

The first two packages should be installed using apt-get on the Raspberry Pi if you're using Raspbian (or some other Debian variant).  The Xvfb package allows for a virtual display to be created so that windows can be rendered in memory.  The Iceweasel package is a branch of the open-source Firefox project which has been modified to run on the Raspberry Pi.  Since the BingScraper script requires Firefox, this branch of Firefox will work just fine.

The Xvfbwrapper package should be installed via pip or easy_install.  It is a Python wrapper around Xvfb.  You can read more about it [here](https://pypi.python.org/pypi/xvfbwrapper/0.2.4).

Running on the Raspberry Pi requires the use of the majority of the Pi's resources.  When I tested the script, it was done so using the original Raspberry Pi, model B+.  In order for the script to be run successfully, the it needed to be executed using the following command line:

python3 BingScraper.py -t 60 -x -b 240 <username> <password>

Because the Raspberry Pi B+ is a single core unit with 512MB of RAM, it was necessary to increase the refresh interval so that web pages would have enough time to be rendered as well as the timeout when connecting to the web browser.

### Contribution guidelines ###

* If you find an issue with the application, please feel free to use the bug tracker to submit a new ticket.
* If you decide to fix an issue that you have found, please create a pull request.
* If you expand upon this script and want the changes to reflect in this repository, please use a pull request.
* Bug fixes and modifications are welcome!

### Who do I talk to? ###

* Benjamin Rood <benjaminjrood@gmail.com>