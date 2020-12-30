#!/usr/bin/env python3

import requests


# Get forecast according to https://opendata.smhi.se/apidocs/metfcst/index.html
class PySmhi:

    def getWeatherStr(self, x): return {
        1:	'Clear sky',
        2:	'Nearly clear sky',
        3:	'Variable cloudiness',
        4:	'Halfclear sky',
        5:	'Cloudy sky',
        6:	'Overcast',
        7:	'Fog',
        8:	'Light rain showers',
        9:	'Moderate rain showers',
        10:	'Heavy rain showers',
        11:	'Thunderstorm',
        12:	'Light sleet showers',
        13:	'Moderate sleet showers',
        14:	'Heavy sleet showers',
        15:	'Light snow showers',
        16:	'Moderate snow showers',
        17:	'Heavy snow showers',
        18:	'Light rain',
        19:	'Moderate rain',
        20:	'Heavy rain',
        21:	'Thunder',
        22:	'Light sleet',
        23:	'Moderate sleet',
        24:	'Heavy sleet',
        25:	'Light snowfall',
        26:	'Moderate snowfall',
        27:	'Heavy snowfall'}.get(x, 'Unknown weather')

    # Get weather forecast
    def getWeatherForecast(self, lat, lng):

        output = []
        url = "http://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/%s/lat/%s/data.json" \
            % (lng, lat)
        try:
            # Get forecast
            r = requests.get(url)
        except Exception:
            print("Url request failed")
            return []
        # Valid response?
        if(not hasattr(r, 'status_code')):
            print("URL return invalid response")
            return []

        if(r.status_code == 200):  # OK
            jw = r.json()
            # iterate the forecast hour by hour starting from now
            for fc_hour in jw['timeSeries']:
                if not fc_hour or "parameters" not in fc_hour:
                    print("Error in response : %s" % (fc_hour))
                else:
                    temp = ws = wgs = rhum = rsym = 126  # default fail

                    for p in fc_hour["parameters"]:
                        param = p["name"]
                        val = p["values"][0]
                        if param == "t":
                            temp = val  # temperature
                        elif param == "ws":
                            ws = val    # Wind speed
                        elif param == "gust":
                            wgs = val   # Wind gust speed
                        elif param == "r":
                            rhum = val  # Relative humidity
                        elif param == "Wsymb2":
                            rsym = self.getWeatherStr(val)  # Weather symbol
                    output.append([temp, ws, wgs, rhum, rsym])
        else:
            print("Url request failed: %s" % (r.status_code))
        return output

    # Get weather
    def getWeather(self, nof_hours, lat, lng):
        wf = self.getWeatherForecast(lat, lng)
        return wf[0:nof_hours]

    # Get weather string
    def getFcStr(self, fc):
        return "temp: {:2.1f}C wind: {:2.1f} ({:2.1f})m/s relHumid: {:3d}%, weahter: {:s}".format(*fc)


# --------------------------------------------------------
if __name__ == "__main__":
    ps = PySmhi()
    # Get current weather in Smygehamn
    w = ps.getWeather(28, 55.348446, 13.360708)
    if w:
        for idx, fc in enumerate(w):
            print("{:2d} {:s}".format(idx, ps.getFcStr(fc)))
