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

### Contribution guidelines ###

* If you find an issue with the application, please feel free to use the bug tracker to submit a new ticket.
* If you decide to fix an issue that you have found, please create a pull request.
* If you expand upon this script and want the changes to reflect in this repository, please use a pull request.
* Bug fixes and modifications are welcome!

### Who do I talk to? ###

* Benjamin Rood <benjaminjrood@gmail.com>