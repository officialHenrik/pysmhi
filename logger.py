#!/usr/bin/env python3

import time
import schedule
from influxdb import InfluxDBClient
from pysmhi import PySmhi

# ------------------------------------------------------
# Influx cfg
USER = 'root'
PASSWORD = 'root'
DBNAME = 'test'
HOST = 'localhost'
PORT = 8086

# ------------------------------------------------------
def get_point(where, lat, lng):
    ps = PySmhi()
    w = ps.getWeather(1, lat, lng) # Get current weather
    point = {
        "measurement": 'Temp',
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
    # Insert into db
    points = []
    p1 = get_point("Smygehamn", 55.348446, 13.360708) # Get current weather
    points.append(p1)
    p2 = get_point("Eklanda", 57.650989, 11.965847) # Get current weather
    points.append(p2)
    print(points)
    client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)

    if(client.write_points(points)):
        points = []
    else:
       	# failure
        print("Warning: failed inserting into influxdb")

        
# ------------------------------------------------------
# Schedule logging
schedule.every(1).hour.do(log_to_db)

# Run forever
try:
    schedule.run_all()
    while True:
       	schedule.run_pending()
        time.sleep(1)
finally:
    print("smhi logger failed...")
