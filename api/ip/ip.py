import requests
from diskcache import Cache

cache = Cache("cache")

@cache.memoize()
def ip_location(ip: str):
    ip_api_res = requests.get(f"http://ip-api.com/json/{ip}?fields=lat,lon")
    ip_api_json = ip_api_res.json()

    try:
        return {
            "ip": ip,
            "lat": ip_api_json["lat"],
            "lon": ip_api_json["lon"]
        }
    except KeyError as ke:  # ip-api didn't return location
        return None
