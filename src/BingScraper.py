'''
A simple Selenium Webdriver module that scrapes Bing to claim reward points.
This uses a word generator sourced from a web page.  The reason for using 
Selenium instead of the page scraping method used by BingRewards is that 
Microsoft changed the web page so that JavaScript is required.

@author: Benjamin Rood
'''

import argparse
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

DELAY   = (5, 10, 15, 20, 25, 30, 60);
PCEXECS = 35;
MBEXECS = 25;
WORDS   = "http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt";

def getWordList( driver, source ):
    """
        Retrieves a list of words to use for queries from the specified source.
        The source is expected to be a web page that renders each word on a
        separate line.
            
        @param driver: The Selenium webdriver object to use
        @return A list of words to use as queries. 
    """
    
    driver.get( source );
    return driver.page_source.split( '\n' );

def login( driver, account, password ):
    """
        Login to a Microsoft account using the supplied credentials.  Once 
        logged in, simply navigate back to www.bing.com in order to start 
        searching.
        
        @param driver: The Selenium webdriver object to use
        @param account: The Microsoft Live account username
        @param password: The password to the Microsoft Live account   
    """
    
    driver.get( "http://login.live.com" );
    
    time.sleep( 2 );
    
    # Get the elements to fill in and the button to click to login.
    
    login = driver.find_element_by_name( 'loginfmt' );
    passw = driver.find_element_by_name( 'passwd' );
    submt = driver.find_element_by_name( 'SI' );
    
    login.send_keys( account );
    passw.send_keys( password );
    
    time.sleep( 2 );
    
    submt.click();
    
def getCredits( driver ):
    """
        Navigate to www.bing.com/rewards/dashboard and parse the number of
        currently earned credits and lifetime credits.
        
        @param driver: The Selenium webdriver object to use
        @return: A tuple that contains the number of current credits, the
                 number of lifetime credits earned, and the percentage towards
                 the currently selected goal.
    """
    
    driver.get( "http://www.bing.com/rewards/dashboard" );
    
    # Waiting a few seconds and refreshing the page seems to allow the login 
    # credentials to propagate properly.
    
    time.sleep( 5 );
    driver.refresh();
    time.sleep( 5 );
    
    # The following statement finds the elements that contain the currently
    # accumulated credits and the lifetime accumulated credits.  The first 
    # element in the list will be the current credits, and the second will be 
    # the lifetime credits.
    
    creds = driver.find_elements_by_class_name( 'credits' );
    perct = driver.find_elements_by_class_name( 'progress-percentage' );
    
    return ( creds[0].text, creds[1].text, perct[0].text );
    
    
def runQuery( driver, query ):
    """
        Executes a query to gain those delicious reward points.
        
        @param driver: The Selenium webdriver object to use
        @param query: The search term to submit to Bing   
    """
    
    driver.get( "http://www.bing.com" );
    
    qinput = driver.find_element_by_name( 'q' );
    qinput.send_keys( query );
    qinput.send_keys( Keys.RETURN );
    
def printReport( bcreds, acreds ):
    """
        Prints a report on the total number of earned credits upon execution of
        this script.
        
        @param bcreds: A hashmap of {'account' : (accumulated, lifetime, %)} before
                       any searches took place
        @param acreds: A hashmap of {'account' : (accumulated, lifetime, %)) after
                       searching
    """

    print( "--------------------------------------------------------------------------------------------------------" );
    print( "| " + "Account".ljust(40) + "| " + "Before".ljust(10) + "| " + "After".ljust(10) + "| " + "Earned".ljust(10) + "| " + "Lifetime".ljust(10) + "| " + "Progress".ljust(10) + " |" );
    
    for key in bcreds:
        before = bcreds[key]; # Tuple: (Credits, Lifetime, %)
        after  = acreds[key]; # Tuple: (Credits, Lifetime, %)
        lftime = after[1];
        pctcmp = after[2];

        print( "| " + key.ljust(40) + "| " + before[0].ljust(10) + "| " + after[0].ljust(10) + "| " + str(int(after[0]) - int(before[0])).ljust(10) + "| " + lftime.ljust(10) + "| " + pctcmp.ljust(10) +  " |" );

    print( "--------------------------------------------------------------------------------------------------------" );

if __name__ == '__main__':
    driver = [];
    bcreds = {};
    acreds = {};
    parser = argparse.ArgumentParser();
    
    parser.add_argument( "username",
                         help = "Specifies the Microsoft account username credential" );
    parser.add_argument( "password",
                         help = "Specifies the Microsoft account password" );
                         
    args = parser.parse_args();
    
    rProfile = webdriver.FirefoxProfile();
    mProfile = webdriver.FirefoxProfile();
    
    mProfile.set_preference( "general.useragent.override", "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0" );
    
    driver.append( webdriver.Firefox( rProfile ) );
    driver.append( webdriver.Firefox( mProfile ) );
    
    words  = getWordList( driver[0], WORDS );

    print( "--------------------------------------------------------------------------------------------------------" );
    print( "Account: " + args.username );
    print( "" );
      
    login( driver[0], args.username, args.password );
    login( driver[1], args.username, args.password );
      
    # After logging in, retrieve the current number of credits before 
    # running searches so that a report can be generated.
      
    credits = getCredits( driver[0] );
    bcreds[args.username] = credits;
      
    # Retrieve the snapshot of credits before running searches, so that a
    # report on the number of credits earned can be generated.
         
    # Run PC Searches - 30 of them will net 15 credits for the day.
    # Delay a random amount before each search so that they don't detect 
    # I'm a robot (or at least have a harder time).
    for i in range( 0, PCEXECS ):
        time.sleep( random.choice( DELAY ) );
        query = random.choice( words );
        print( "Performing PC search " + str( (i + 1) ) + "/" + str( PCEXECS ) + ": " + query );
        runQuery( driver[0], query );
    
    print( "" );
        
    # Run mobile platform searches - 20 of them will net 10 credits for the
    # day.  As stated above, delay a random amount before each search so 
    # that they don't detect I'm a robot (or at least have a harder time).
        
    for i in range( 0, MBEXECS ):
        time.sleep( random.choice( DELAY ) );
        query = random.choice( words );
        print( "Performing Mobile search " + str( (i + 1) ) + "/" + str( MBEXECS ) + ": " + query );
        runQuery( driver[1], query );

    print( "--------------------------------------------------------------------------------------------------------" );

    # Retrieve the number of credits after performing searches, so an
    # effective report may be generated.
      
    credits = getCredits( driver[0] );
    acreds[args.username] = credits;
    
    driver[0].close();
    driver[1].close();
    
    # Print an effective report on the number of credits earned with this 
    # execution.
    
    printReport( bcreds, acreds );