import sqlite3
import csv

db_connect = sqlite3.connect('external_partners.db')
db_cursor = db_connect.cursor()

def select_all():
    db_cursor.execute("SELECT count(advertiser) FROM externalRevenue_dedupe WHERE date >= 32317 AND date <= 32717" )
    # db_cursor.execute("SELECT * FROM externalRevenue_dedupe" )
    with open('test_report.csv',w) as test_report:
        for row in db_cursor.fetchall():
            test_report = csv.writer(row)

def update_column():
    db_cursor.execute("UPDATE test_table SET advertiser = 'Maple Digital' WHERE advertiser = 'Maple Digitial'")
    db_connect.commit()

def alter_table():
    db_cursor.execute("CREATE TABLE externalRevenue (date DATE NOT NULL, advertiser TEXT, platform TEXT, impression REAL, revenue REAL)")
    db_cursor.execute("INSERT INTO externalRevenue (date,advertiser,impression,revenue) SELECT date, advertiser, impression, revenue FROM test_table")
    db_cursor.execute("DROP TABLE test_table")
    db_cursor.execute("UPDATE externalRevenue SET platform = 'LKQD'")
    db_connect.commit()

def create_table():
    db_cursor.execute("CREATE TABLE externalRevenue_dedupe (date DATE NOT NULL, advertiser TEXT, platform TEXT, impression REAL, revenue REAL)")
    db_connect.commit()

def dedupe_table():
    db_cursor.execute("INSERT INTO externalRevenue_dedupe SELECT DISTINCT * FROM externalRevenue")
    db_connect.commit()

dedupe_table()
