'''
Creator: Andrew Ravn

Purpose:
Module will initialize, access, and update SQLite database holding our partner numbers. This will be used for analysis as well as comparison with internal numbers.
'''
import sqlite3
import os

class Abstract_Create_DB(object):

    def __init__(self, db_name):

        self.db_name = db_name


class Access_DB(Abstract_Create_DB):
    '''
    Class accesses DB, if the DB does not currently exist, we will create it
    '''
    def __init__(self, db_name):
        super().__init__(db_name)

    def create_db(self):

        create = not os.path.exists(self.db_name)
        reporting_db = sqlite3.connect(self.db_name)
        if create:
            c = reporting_db.cursor()
            # Create table, each player should be unique and not empty, we have set up the column to be unique and not allowed to equal null
            c.execute("CREATE TABLE externalRevenue (date DATE NOT NULL, advertiser TEXT, platform TEXT, impression REAL, revenue REAL)")
            reporting_db.commit()
        return reporting_db

    def load(self, record):
        db_connect = Access_DB.create_db(self)
        db_cursor = db_connect.cursor()
        # Loads data from record in format below, if there is an error in the data, we continue running through with option to print out a error message for the user.
        # Record is loaded as a dictionary
        try:
            db_cursor.execute("INSERT INTO externalRevenue (date, "
                              "advertiser, "
                              "platform, "
                              "impression, "
                              "revenue) "
                              "VALUES (:Date, "
                              ":Advertiser, "
                              ":Platform, "
                              ":Impression, "
                              ":Revenue)", record)

        except sqlite3.IntegrityError:
            pass
        db_connect.commit()
        db_connect.close()
