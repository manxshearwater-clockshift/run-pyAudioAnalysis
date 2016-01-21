import csv
import sqlite3

DB_NAME = "birds_sqlite.sqlite"

# COLUMN NAMES
BIRD = "bird"
YEAR = "year"
MONTH = "month"
DAY = "day"
HOUR = "hour"
MINUTE = "minute"
SECOND = "second"
CLASS = "class"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='TABLE_BIRDS'")
    print(c.fetchall())
    if c.arraysize < 2:
        c.execute("CREATE TABLE TABLE_BIRDS (BIRD TEXT, YEAR INTEGER, MONTH INTEGER, DAY INTEGER, HOUR INTEGER, "
                  "MINUTE INTEGER, SECOND INTEGER, CLASS INTEGER)")
    conn.commit()
    conn.close()

def drop_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE TABLE_BIRDS")
    conn.commit()
    conn.close()

def csv_to_db(csvfilename, bird):
    with open(csvfilename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.next()  # skip header
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        for row in reader:
            dt = [row[0], row[1], row[2], row[3], row[4], row[5]]
            c.execute("INSERT INTO TABLE_BIRDS VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (bird, dt[0], dt[1], dt[2], dt[3],
              dt[4], dt[5], row[6]))
        conn.commit()
        conn.close()

def get_one_day(bird_table_name, daynr):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT class FROM TABLE_BIRDS WHERE DAY=?", (daynr, ))
    day = c.fetchall()
    conn.close()
    return day

def get_one_hour(bird, daynr, hour):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT class FROM TABLE_BIRDS WHERE DAY=? AND HOUR=?", (daynr, hour, ))
    hour = c.fetchall()
    conn.close()
    return hour

def get_all_from_bird(bird):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM TABLE_BIRDS")
    bird = c.fetchall()
    conn.close()
    return bird
