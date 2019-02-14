#! /usr/bin/python

import requests
import json

class PySmhi:
            
    def getWeather(self, lat, lng):
        url = "http://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/%s/lat/%s/data.json" % (lng, lat)

        r = requests.get(url)

        output = [126, 126, 126] # default failure
        nof_vals = 0

        if(r.status_code == 200): #OK
            
            o = json.loads(r.text)
            for w in o['timeSeries']:
                nof_vals+=1
                if not w or not "parameters" in w:
                    print("Error in response : %s" % (w))
                else:
                    for p in w["parameters"]:
                        if p["name"] == "t":
                            temp = float(p["values"][0])
                        if p["name"] == "ws":
                            ws = float(p["values"][0])
                        if p["name"] == "r":
                            rhum = float(p["values"][0])
                    output = [temp, ws, rhum]
                
                break;
        else:
            print("Url request failed : %s" % (r.status_code))
        return(output)
 
ps = PySmhi()
w = ps.getWeather(55.348446, 13.360708) # in Smygehamn
 
print("temp: {}C, wind: {}m/s, relHumid: {}%".format(w[0],w[1],w[2]))