#!/usr/bin/env python3

import time
import schedule
from influxdb import InfluxDBClient
from pysmhi import PySmhi
from datetime import datetime

# ------------------------------------------------------
# Influx cfg
USER = 'root'
PASSWORD = 'root'
DBNAME = 'test'
HOST = 'localhost'
PORT = 8086

points = []

# ------------------------------------------------------
def get_point(where, lat, lng):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    ps = PySmhi()
    w = ps.getWeather(1, lat, lng) # Get current weather
    if w:
        point = {
            "measurement": 'Temp',
            "time": current_time,
            "tags": {
                "location": where,
                "sensor": "smhi", 
            },
            "fields": {
                "temp": w[0][0],
                "wind": w[0][1],
                "gust": w[0][2],
                "humi": w[0][3]
                }
            }
    return(point)

# ------------------------------------------------------
# Callback for writing data to database
def log_to_db():
    global points

    p1 = get_point("Smygehamn", 55.348446, 13.360708) # Get current weather
    points.append(p1)
    p2 = get_point("Eklanda", 57.650989, 11.965847) # Get current weather
    points.append(p2)

    try:
        client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)

        if(client.write_points(points)):
            points = []
        else:
            print("Warning: failed inserting into influxdb")
    except:
        print("Influx connection failed")

# ------------------------------------------------------
# Schedule logging
schedule.every(15).minutes.do(log_to_db)

# Run forever
try:
    schedule.run_all()
    while True:
        try:
       	    schedule.run_pending()
        except:
            print("pysmhi failed, continuing")
        time.sleep(1)
finally:
    print("ERROR: pysmhi logger failed...")
