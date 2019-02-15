#!/usr/bin/env python3

import requests

class PySmhi:
    # Get weather forecast
    def getWeatherForecast(self, lat, lng):

        output = []
        # Get forecast according to https://opendata.smhi.se/apidocs/metfcst/index.html
        url = "http://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/%s/lat/%s/data.json" % (lng, lat)
        r = requests.get(url)

        if(r.status_code == 200): #OK
            jw = r.json()
            # iterate the forecast hour by hour
            for fc_hour in jw['timeSeries']:
                if not fc_hour or not "parameters" in fc_hour:
                    print("Error in response : %s" % (fc_hour))
                else:
                    temp = ws = wgs = rhum = 126 # default fail
                    for p in fc_hour["parameters"]:
                        param = p["name"]
                        val   = p["values"][0]
                        if param == "t":      temp = val # temperature
                        elif param == "ws":   ws = val   # Wind speed
                        elif param == "gust": wgs = val  # Wind gust speed
                        elif param == "r":    rhum = val # Relative humidity
                    output.append([temp, ws, wgs, rhum])
        else:
            print("Url request failed: %s" % (r.status_code))
        return(output)

    # Get weather
    def getWeather(self, nof_hours, lat, lng):
        wf = self.getWeatherForecast(lat, lng)
        return(wf[0:nof_hours])

# --------------------------------------------------------
if __name__ == "__main__":
    ps = PySmhi()
    w = ps.getWeather(1, 55.348446, 13.360708) # Get current weather in Smygehamn
    if w:
        for f in w:
            print("temp: {}C, wind: {}({})m/s, relHumid: {}%".format(fc[0],fc[1],fc[2],fc[3]))
