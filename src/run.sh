#!/usr/bin/env bash
#
# A script to run the BingScraper Python script, generate a report,
# and send the report via email.
#
# Date: January 28, 2016

WORKDIR=`mktemp -d`
REPORTFILE=$WORKDIR/report.txt
OUTPUTFILE=$WORKDIR/output.txt
SCRIPT=./BingScraper.py
PYTHON=`which python`
DATE=`date`
RUN=1

function print()
{
	echo "$1" | tee -a $OUTPUTFILE
}

function printn()
{
	echo -n "$1" | tee -a $OUTPUTFILE
}

# Uncomment and set directory to the location of the BingScraper script if 
# running as a cron job.
#cd /home/pi/Downloads/bingscraper/src

# Uncomment if the output of the script is to be sent in an email report.
#print "Subject: BingScraper Report for $DATE"
#print ""
#print ""
printn "Checking for python..."

if [[ ! -f $PYTHON ]];
then
	print ""
	print "[ERROR] Python not found."
	print ""
	RUN=0
fi

if [[ $RUN -eq 1 ]];
then
	printn "[OK]"
	print ""
	print "Executing BingScraper script..."

	$PYTHON $SCRIPT "$1" "$2" | tee -a $REPORTFILE
fi

cat $REPORTFILE >> $OUTPUTFILE

# Uncomment if the report is to be sent to an email address.  You must configure
# ssmtp before using this.
#/usr/sbin/ssmtp iamsomeuser@gmail.com < $OUTPUTFILE

