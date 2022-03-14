import sqlite3
from sqlite3 import Error

from numpy import int32


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def create_table():
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS bookings")
    sql ='''CREATE TABLE bookings(
    booking_id INT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    pick_up_point TEXT NOT NULL,
    destination TEXT NOT NULL,
    longitude FLOAT,
    latitude FLOAT 
    )'''
    cursor.execute(sql)
    conn.commit()
    conn.close()
def get_data():
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE booking_id=?",(3,))
    results = cursor.fetchall()
    print(results)


if __name__ == '__main__':
    #create_connection(r"/Users/Jaswin/Desktop/MS_assessment_Q2.nosync/question 2/bookings.db")
    #create_table()
    get_data()
