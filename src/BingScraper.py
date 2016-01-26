'''
A simple Selenium Webdriver module that scrapes Bing to claim reward points.
This uses a word generator sourced from a web page.  The reason for using 
Selenium instead of the page scraping method used by BingRewards is that 
Microsoft changed the web page so that JavaScript is required.

@author: Benjamin Rood
'''

import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

DELAY   = (5, 10, 15, 20, 25, 30, 60);
PCEXECS = (40, 50, 60);
MBEXECS = (30, 40, 50);
WORDS   = "http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt";

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
    
def getCredits( driver ):
    """
        Navigate to www.bing.com/rewards/dashboard and parse the number of
        currently earned credits and lifetime credits.
        
        @param driver: The Selenium webdriver object to use
        @return: A tuple that contains the number of current credits and the
                 number of lifetime credits earned.
    """
    
    driver.get( "http://www.bing.com/rewards/dashboard" );
    
    # Waiting a few seconds and refreshing the page seems to allow the login 
    # credentials to propagate properly.
    
    time.sleep( 3 );
    driver.refresh();
    time.sleep( 3 );
    
    # The following statement finds the elements that contain the currently
    # accumulated credits and the lifetime accumulated credits.  The first 
    # element in the list will be the current credits, and the second will be 
    # the lifetime credits.
    
    creds = driver.find_elements_by_class_name( 'credits' );
    
    return ( creds[0].text, creds[1].text );
    
    
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
        
        @param bcreds: A hashmap of {'account' : (accumulated, lifetime)} before
                       any searches took place
        @param acreds: A hashmap of {'account' : (accumulated, lifetime)) after
                       searching
    """
    
    print( "---------------------------------------------------------------" );
    print( "Credit Report:" );
    print( "" );
    print( "| " + "Account".ljust(40) + "| " + "Before".ljust(10) + "| " + "After".ljust(10) + "| " + "Earned".ljust(10) + "| " + "Lifetime".ljust(10) + " |");
    
    for key in bcreds:
        before = bcreds[key]; # Tuple: (Credits, Lifetime)
        after  = acreds[key]; # Tuple: (Credits, Lifetime)
        lftime = after[1];
        
        print( "| " + key.ljust(40) + "| " + before[0].ljust(10) + "| " + after[0].ljust(10) + "| " + str(int(after[0]) - int(before[0])).ljust(10) + "| " + lftime.ljust(10) + " |" );
        
    print( "---------------------------------------------------------------" );    

if __name__ == '__main__':
    driver = webdriver.Firefox();
    words  = getWordList( driver, WORDS );
    bcreds = {};
    acreds = {};
    
    for accountPair in ACCOUNTS:
        if (driver == None):
            driver = webdriver.Firefox();
            
        username = accountPair[0];
        password = accountPair[1];
        pcexecs  = random.choice( PCEXECS );
        mbexecs  = random.choice( MBEXECS );
        
        print( "---------------------------------------------------------------" );
        print( "Account: " + username );
        print( "" );
        
        login( driver, username, password );
        
        # After logging in, retrieve the current number of credits before 
        # running searches so that a report can be generated.
        
        credits = getCredits( driver );
        bcreds[username] = credits;
        
        # Retrieve the snapshot of credits before running searches, so that a
        # report on the number of credits earned can be generated.
         
        # Run PC Searches - 30 of them will net 15 credits for the day.
        # Delay a random amount before each search so that they don't detect 
        # I'm a robot (or at least have a harder time).
        for i in range( 0, pcexecs ):
            time.sleep( random.choice( DELAY ) );
            query = random.choice( words );
            print( "Performing PC search " + str( (i + 1) ) + "/" + str( pcexecs ) + ": " + query );
            runQuery( driver, query );

        print( "" );
        
        driver.close();
        
        # Run mobile platform searches - 20 of them will net 10 credits for the
        # day.  As stated above, delay a random amount before each search so 
        # that they don't detect I'm a robot (or at least have a harder time).
        profile = webdriver.FirefoxProfile();
        profile.set_preference( "general.useragent.override", "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0" );
        driver  = webdriver.Firefox( profile );
        
        login( driver, username, password );
        
        for i in range( 0, mbexecs ):
            time.sleep( random.choice( DELAY ) );
            query = random.choice( words );
            print( "Performing Mobile search " + str( (i + 1) ) + "/" + str( mbexecs ) + ": " + query );
            runQuery( driver, query );        
        
        print( "---------------------------------------------------------------" );
        
        # Closing the driver effectively logs out.  A bit inefficient, but it
        # works pretty well.
        driver.close();
        driver = None;
        
        # Login again, so that we can retrieve the number of credits earned.
        driver = webdriver.Firefox();
        login( driver, username, password );
        
        # Retrieve the number of credits after performing searches, so an 
        # effective report may be generated.
        
        credits = getCredits( driver );
        acreds[username] = credits;
        
        driver.close();
        driver = None;
        
    # Print an effective report on the number of credits earned with this 
    # execution.
    
    printReport( bcreds, acreds );