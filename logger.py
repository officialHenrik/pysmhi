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


ps = PySmhi()

# ------------------------------------------------------
# Callback for writing data to database
def log_to_db():
    
    points = []
    # get data
    ps = PySmhi()
    #w = ps.getWeather(1, 55.348446, 13.360708) # Get current weather in Smygehamn
    w = ps.getWeather(1, 57.650989, 11.965847) # Get current weather in Eklanda
    temp = w[0][0]
    wind = w[0][1]
    gust = w[0][2]
    humi = w[0][3]
    
    # Insert into db
    point = {
        "measurement": 'Temp',
        "tags": {
            "location": "home",
            "sensor": "smhi", 
        },
        "fields": {
             "temp": temp,
             "wind": wind,
             "gust": gust,
             "humi": humi
                }
            }
    points.append(point)
    
    client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)

    if(client.write_points(points)):
        points = []
    else:
       	# failure, try again next time
        print("Warning: failed inserting into influxdb")

# Schedule logging
schedule.every(1).hour.do(log_to_db)

# ------------------------------------------------------
# Run forever
try:
    schedule.run_all()
    while True:
       	schedule.run_pending()
        time.sleep(1)
finally:
    print("smhi logger failed...")