#! /usr/bin/python

import requests
import json

class PySmhi:
        
    # Get weather forecast
    def getWeatherForecast(self, lat, lng):
  
        output = []      
        # Get forecast according to https://opendata.smhi.se/apidocs/metfcst/index.html
        url = "http://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/%s/lat/%s/data.json" % (lng, lat)
        r = requests.get(url)

        if(r.status_code == 200): #OK
            o = json.loads(r.text)
            # iterate the forecast
            for w in o['timeSeries']:
                if not w or not "parameters" in w:
                    print("Error in response : %s" % (w))
                else:
                    temp = ws = wgs = rhum = 126
                    for p in w["parameters"]:
                        param = p["name"]
                        val   = p["values"][0]
                        if param == "t": # Temperature
                            temp = val
                        if param == "ws": # Wind speed
                            ws = val
                        if param == "gust": # Wind gust speed
                            wgs = val
                        if param == "r": # Relative humidity
                            rhum = val
                    output.append([temp, ws, wgs, rhum])
        else:
            print("Url request failed: %s" % (r.status_code))
        return(output)
        
    # Get weather
    def getWeather(self, nof, lat, lng):
        wf = self.getWeatherForecast(lat, lng)
        return(wf[0:nof])

if __name__ == "__main__":
    ps = PySmhi()
    w = ps.getWeather(1, 55.348446, 13.360708) # Get current weather in Smygehamn
    if w:
        for fc in w:
            print("temp: {}C, wind: {}({})m/s, relHumid: {}%".format(fc[0],fc[1],fc[2],fc[3]))
