import requests
from datetime import datetime

API_TIMEOUT = 8
FORECAST_DAYS = 3
HOURLY_WINDOW = 12

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WX_URL = "https://api.open-meteo.com/v1/forecast"


def fmt(value):
    """Format a number to one decimal place, or '?' if invalid."""
    try:
        return f"{float(value):.1f}"
    except (TypeError, ValueError):
        return "?"


def to_fahrenheit(celsius):
    """Convert a Celsius value to Fahrenheit, passing through None."""
    return None if celsius is None else (celsius * 9 / 5) + 32


def safe_get(url, params):
    """Make a GET request and return parsed JSON, or exit on error."""
    try:
        response = requests.get(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise SystemExit(f"Error retrieving data: {exc}")


def geocode(city):
    """Resolve a city name to (name, latitude, longitude)."""
    data = safe_get(GEO_URL, {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    })
    results = data.get("results")
    if not results:
        raise SystemExit(f"City not found: {city}")
    top = results[0]
    return top["name"], top["latitude"], top["longitude"]


def get_weather(lat, lon):
    """Fetch current, daily, and hourly weather for a coordinate."""
    return safe_get(WX_URL, {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "hourly": ["temperature_2m"],
        "forecast_days": FORECAST_DAYS,
    })


def slice_next_hours(hourly, count):
    """Return up to `count` (time, temp) pairs starting from the current hour."""
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    now = datetime.now()

    start = 0
    for i, t in enumerate(times):
        if datetime.fromisoformat(t) >= now:
            start = i
            break

    return list(zip(times[start:start + count], temps[start:start + count]))


def main():
    city = input("Enter your city: ").strip() or "Kathmandu"
    unit = input("Enter your temperature unit (C/F): ").strip().upper() or "C"
    if unit not in ("C", "F"):
        unit = "C"

    name, lat, lon = geocode(city)
    wx = get_weather(lat, lon)

    convert = to_fahrenheit if unit == "F" else (lambda c: c)

    # Current
    current = wx.get("current_weather", {})
    temp_now = convert(current.get("temperature"))
    print(f"\n{name}: {fmt(temp_now)}°{unit}")

    # Next 12 hours
    hourly = slice_next_hours(wx.get("hourly", {}), HOURLY_WINDOW)
    if hourly:
        print(f"\nNext {len(hourly)} hours:")
        for time_str, temp in hourly:
            label = datetime.fromisoformat(time_str).strftime("%H:%M")
            print(f"  {label}  {fmt(convert(temp))}°{unit}")

    # Daily
    daily = wx.get("daily", {})
    dates = daily.get("time", []) or []
    highs = daily.get("temperature_2m_max", []) or []
    lows = daily.get("temperature_2m_min", []) or []

    print(f"\n{FORECAST_DAYS}-day forecast:")
    for date, hi, lo in zip(dates, highs, lows):
        hi, lo = convert(hi), convert(lo)
        print(f"  {date}: {fmt(lo)}°{unit} → {fmt(hi)}°{unit}")


if __name__ == "__main__":
    main()