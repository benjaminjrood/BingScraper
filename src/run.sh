#!/usr/bin/env bash
#
# A script to run the BingScraper Python script, generate a report,
# and send the report via email.
#
# Date: January 4, 2016

WORKDIR=`mktemp -d`
REPORTFILE=$WORKDIR/report.txt
OUTPUTFILE=$WORKDIR/output.txt
SCRIPT=./BingScraper.py
PYTHON=`which python`
DATE=`date`
RUN=1

function print()
{
	echo "$1" >> $OUTPUTFILE
}

function printn()
{
	echo -n "$1" >> $OUTPUTFILE
}

cd /home/pi/Downloads/bingscraper/src

print "Subject: BingScraper Report for $DATE"
print ""
print ""
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
	printn "Executing BingScraper script..."

	$PYTHON $SCRIPT > $REPORTFILE & wait

	printn "[DONE]"
	print ""
	print ""
	print "Output:"
	print ""
fi

cat $REPORTFILE >> $OUTPUTFILE

/usr/sbin/ssmtp EMAIL_HERE < $OUTPUTFILE

