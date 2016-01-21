'''
A simple Selenium Webdriver module that scrapes Bing to claim reward points.
This uses a word generator sourced from a web page.  The reason for using 
Selenium instead of the page scraping method used by BingRewards is that 
Microsoft changed the web page so that JavaScript is required.

@author: Benjamin Rood
'''

import random
import time
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

DELAY = (1, 5, 10, 15, 20, 25, 30);
WORDS = "http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt";

# Add accounts as tuples of (username, password).
ACCOUNTS = (("Imaliveaccount@gmail.com", "Imapassword"), 
            ("Anotheraccount@gmail.com", "anotherpassword"));

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
    
    # Get the elements to fill in and the button to click to login.
    
    login = driver.find_element_by_name( 'loginfmt' );
    passw = driver.find_element_by_name( 'passwd' );
    submt = driver.find_element_by_name( 'SI' );
    
    login.send_keys( account );
    passw.send_keys( password );
    submt.click();   
    
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

if __name__ == '__main__':
    driver = webdriver.Firefox();
    words  = getWordList( driver, WORDS );
    
    for accountPair in ACCOUNTS:
        if (driver == None):
            driver = webdriver.Firefox();
            
        username = accountPair[0];
        password = accountPair[1];
        
        print "---------------------------------------------------------------";
        print "Account: " + username;
        print "";
        
        login( driver, username, password );
         
        # Run PC Searches - 30 of them will net 15 credits for the day.
        # Delay a random amount before and after each search so that they 
        # don't detect I'm a robot.
        for i in range(0, 30):
            time.sleep( random.choice( DELAY ) );
             
            query = random.choice( words );
             
            print "Performing PC search " + str( i ) + "/30: " + query;
            runQuery( driver, query );
             
            time.sleep( random.choice( DELAY ) );

        print "";
        
        driver.close();
        
        # Run mobile platform searches - 20 of them will net 10 credits for the
        # day.  As stated above, delay a random amount before and after each
        # search so that they don't detect I'm a robot.
        profile = webdriver.FirefoxProfile();
        profile.set_preference( "general.useragent.override", "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0" );
        driver  = webdriver.Firefox( profile );
        
        login( driver, username, password );
        
        for i in range(0, 20):
            time.sleep( random.choice( DELAY ) );
             
            query = random.choice( words );
             
            print "Performing Mobile search " + str( i ) + "/20: " + query;
            runQuery( driver, query );
             
            time.sleep( random.choice( DELAY ) );
        
        
        print "---------------------------------------------------------------";
        # Closing the driver effectively logs out.  A bit inefficient, but it
        # works pretty well.
        driver.close();
        driver = None;