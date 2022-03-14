from pydantic import BaseModel, Field
import requests
import sqlite3
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS

info = Info(title='Taxi booking API', version='1.0.0')
app = OpenAPI(__name__, info=info)
CORS(app)

taxi_tag = Tag(name='Taxi Booking', description='Booking Taxi services')

class BookingPath(BaseModel):
    bid: int = Field(..., description='booking id')

class BookQuery(BaseModel):
    booking_id: int
    date: str
    time: str
    pick_up_point: str
    destination : str

@app.post('/add_booking', tags=[taxi_tag])
def add_booking(query: BookQuery):
    r = requests.get('https://api.freegeoip.app/json/?apikey=7322ce70-2741-11ec-a395-7f2b5c241db6')
    data = r.json()
    long = data["longitude"]
    lat = data["latitude"]
    #Connecting to sqlite
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    sqlite_insert_query = """INSERT INTO bookings
                          (booking_id, date, time, pick_up_point, destination, longitude,latitude) 
                           VALUES (?,?,?,?,?,?,?)"""
    cursor.execute(sqlite_insert_query, (query.booking_id,query.date,query.time,query.pick_up_point,query.destination,long,lat))
    conn.commit()
    return {
        "message": "Booking made and committed to database",
        "Booking": 
                {"Booking_id":query.booking_id, "Date": query.date, "time": query.time, "Pick up point": query.pick_up_point, "Destination" :query.destination,
                "Current_Location_Latitude" : long, "Current_Location_Longitude": lat}
    }

@app.get('/view_booking/<int:bid>', tags=[taxi_tag])
def view_booking(path: BookingPath):
    if path.bid !=None:
        conn = sqlite3.connect('bookings.db')
        cursor = conn.cursor()
        sqlite_query = """SELECT * FROM bookings WHERE booking_id = ?"""
        cursor.execute(sqlite_query, (path.bid,))
        results = cursor.fetchall()
        return{
            'message:' : 'Returned Requested Booking by booking id',
            'booking':results}

@app.get('/view_all_bookings', tags=[taxi_tag])
def view_all_bookings():
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    results = cursor.fetchall()
    return {'bookings':results,
        'message:' : 'Returned all Bookings'}


@app.post('/update_booking/', tags=[taxi_tag])
def update_booking(query: BookQuery):
    r = requests.get('https://api.freegeoip.app/json/?apikey=7322ce70-2741-11ec-a395-7f2b5c241db6')
    data = r.json()
    long = data["longitude"]
    lat = data["latitude"]
    #Connecting to sqlite
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    sqlite_query = """DELETE FROM bookings WHERE booking_id = ?"""
    cursor.execute(sqlite_query, (query.booking_id,))
    conn.commit()
    sqlite_insert_query = """INSERT INTO bookings
                          (booking_id, date, time, pick_up_point, destination, longitude,latitude) 
                           VALUES (?,?,?,?,?,?,?)"""
    cursor.execute(sqlite_insert_query, (query.booking_id,query.date,query.time,query.pick_up_point,query.destination,long,lat))
    conn.commit()
    return {
        "message": "Booking updated and committed to database",
        "Booking": 
                {"Booking_id":query.booking_id, "Date": query.date, "time": query.time, "Pick up point": query.pick_up_point, "Destination" :query.destination,
                "Current_Location_Latitude" : long, "Current_Location_Longitude": lat}
    }

@app.delete('/delete_booking/<int:bid>', tags=[taxi_tag])
def delete_booking(path: BookingPath):
    if path.bid !=None:
        conn = sqlite3.connect('bookings.db')
        cursor = conn.cursor()
        sqlite_query = """DELETE FROM bookings WHERE booking_id = ?"""
        cursor.execute(sqlite_query, (path.bid,))
        conn.commit()
        return 'Booking deleted'


if __name__ == '__main__':
    app.run()
