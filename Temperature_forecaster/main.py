import requests

def fmt(v):
    try:
        return f"{float(v):.1f}"
    except (TypeError, ValueError):
        return "?"
    
def safe_get(url, params):
    """Make a GET request and return JSON (dict), or None on error."""
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        return r
    except requests.RequestException:
        print("Error retrieving data")
        exit()

city = input("Enter your city: ").strip() or "Kathmandu"

geo_url = "https://geocoding-api.open-meteo.com/v1/search"

params = {
    "name": city,
    "count": 1,
    "language": "en",
    "format": "json"
}

r = safe_get(geo_url, params)

data = r.json()

print("Raw geocoding JSON:", data)

if not data.get("results"):
    print("City not found.")
    exit()

top = data["results"][0]

lat, lon = top["latitude"], top["longitude"]

print("Coords:", lat, lon)

wx_url = "https://api.open-meteo.com/v1/forecast"

wx_params = {
    "latitude": lat,
    "longitude": lon,
    "current_weather": True,
    "timezone": "auto",
    "daily": ["temperature_2m_max", "temperature_2m_min"],
    "forecast_days": 3
}

w = safe_get(wx_url, params=wx_params)

wx = w.json()

cw = wx.get("current_weather", {})

temp_now = cw.get("temperature")

summary_line = f"{city}: {fmt(temp_now)}°C"

print(summary_line)

daily = wx.get("daily", {})
dates = daily.get("time", []) or []
tmax = daily.get("temperature_2m_max", []) or []
tmin = daily.get("temperature_2m_min", []) or []

print("\n3-day Forecast:")
for date, hi, lo in zip(dates, tmax, tmin):
    print(f"{date}: {fmt(lo)}°C → {fmt(hi)}°C")

