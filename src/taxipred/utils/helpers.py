import requests 
from urllib.parse import urljoin
from taxipred.utils.constants import WEATHER_API_KEY, GOOGLE_MAPS_API_KEY


def read_api_endpoint(endpoint = "/", base_url = "http://127.0.0.1:8000"):
    # om base_url skulle vara http://127.0.0.1:8000/api, så skulle "taxi" blir http://127.0.0.1:8000/api/taxi
    # men "/taxi" skulle bli http://127.0.0.1:8000/taxi, då den ersätter pathen
    # alltså skicka inte in "endpoint" med "/" före, om du inte vill ersätta alla "/" efter "porten"(:8000) i base_url
    # urljoin lägger automatiskt till "/" före och efter endpoint
    url = urljoin(base_url, endpoint)
    response = requests.get(url)
    
    return response

# TODO:
# post_api_endpoint
def taxi_prediction_endpoint(payload, endpoint = "taxi/predict", base_url = "http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    response = requests.post(url, json=payload)
    
    return response


def autocomplete_addresses(query):
    url = (
        f"https://maps.googleapis.com/maps/api/place/autocomplete/json"
        f"?input={query}"
        f"&types=address"
        f"&components=country:se"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    description = [p["description"] for p in data.get("predictions", [])]

    return description


def get_travel_route(pickup, dropoff, pickup_timestamp):
    
    # traffic, distance, duration = requests.get()  - skicka med datum och tid?
    response = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={pickup}&destination={dropoff}&departure_time={pickup_timestamp}&key={GOOGLE_MAPS_API_KEY}")

    legs = response.json()["routes"][0]["legs"][0]
    distance = float(legs["distance"]["text"].strip(" km"))
    # 4 hours, ta bort hours, och gör 4*60 för att göra till minuter, plussa med mins, gör detta för duration och duration_in traffic
    duration = float(legs["duration"]["text"].strip(" mins"))
    duration_in_traffic = float(legs["duration_in_traffic"]["text"].strip(" mins"))
    end_address = legs["end_address"]
    
    if duration_in_traffic < duration:
        traffic = "Low"
    elif duration_in_traffic > duration:
        traffic = "High"
    else:
        traffic = "Medium"

    return distance, duration, traffic, end_address


def get_weather(pickup_timestamp, end_address):
    city = end_address.split(", ")[1]
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city},se&appid={WEATHER_API_KEY}&units=metric")
    
    data = response.json()
    closest = min(data["list"], key=lambda x: abs(x["dt"] - pickup_timestamp))

    return closest["weather"][0]["main"]

