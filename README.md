# Automated_Reporting
The purpose of this program is to create a series of web drivers that scrape all of our 3rd party partners' data. It currently
supports LKQD, Vera, and Streamrail platforms. 

There are a couple things that still need work:
1. More robust error handling
2. Figure out why the wait() methods in Selenium don't work as intended sometimes.
3. Setup mySQL or PostgreSQL database instead of SQLite3. SQLite was used as a proof of concept and I already had a .py written to create it from one of my Grad School classes.
