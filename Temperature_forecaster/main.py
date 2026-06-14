import requests

def fmt_temp(value):
    try:
        return f"{float(value):.1f}"
    
    except (TypeError, ValueError):
         return "?"
        

def safe_get(url,params):
    try:
        r=requests.get(url,params=params,timeout=8)
        r.raise_for_status()

        return r
    
    except requests.RequestException:
         print("Error retrieving data")
         exit()

#city api

city=input("Enter your city:")
if city=="":
    city='Kathmandu'
geo_url='https://geocoding-api.open-meteo.com/v1/search'
params={
"name": city,
"count": 1,
"language": "en",
"format": "json"
}

r=requests.get(geo_url,params,timeout=5)
data=r.json()
print("Raw geocoding JSON:", data)

if not data.get("results"):
    print("City not found.")
    exit()

#coordinates

top = data["results"][0]
lat,lon = top["latitude"],top["longitude"]
print("Coords:", lat, lon)

#weather api

wx_url="https://api.open-meteo.com/v1/forecast"

wx_params={
"latitude": lat,
"longitude":lon,
"current_weather":True,
"timezone":"auto"
}
w=requests.get(wx_url,wx_params,timeout=5)
wx=w.json()

#current weather

cw=wx.get("current_weather",{})
temp_now=cw.get("temperature")

summary_line = f"{city}: {temp_now}°C"

print(summary_line)