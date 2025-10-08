import requests 
from urllib.parse import urljoin
from taxipred.utils.constants import WEATHER_API_KEY, GOOGLE_MAPS_API_KEY


def read_api_endpoint(endpoint = "/", base_url = "http://backend:8000"):
    # om base_url skulle vara http://127.0.0.1:8000/api, så skulle "taxi" blir http://127.0.0.1:8000/api/taxi
    # men "/taxi" skulle bli http://127.0.0.1:8000/taxi, då den ersätter pathen
    # alltså skicka inte in "endpoint" med "/" före, om du inte vill ersätta alla "/" efter "porten"(:8000) i base_url
    # urljoin lägger automatiskt till "/" före och efter endpoint
    url = urljoin(base_url, endpoint)
    response = requests.get(url)
    
    return response


def post_api_endpoint(payload, endpoint = "/", base_url = "http://backend:8000"):
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


def get_map(pickup, dropoff):
    return f"https://www.google.com/maps/embed/v1/directions?key={GOOGLE_MAPS_API_KEY}&origin={pickup}&destination={dropoff}&mode=driving"


def get_travel_route(pickup, dropoff, pickup_timestamp):
    response = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={pickup}&destination={dropoff}&departure_time={pickup_timestamp}&key={GOOGLE_MAPS_API_KEY}")

    legs = response.json()["routes"][0]["legs"][0]

    # convert distance and duration values from m and s to km and min
    distance = float(round(legs["distance"]["value"]/1000))
    duration = float(round(legs["duration"]["value"]/60))
    duration_in_traffic = float(round(legs["duration_in_traffic"]["value"]/60))
    # hämta ut end_address för att använda till väder api, då den valda addressen ibland inte innehåller själva staden, men det gör end_address
    end_address = legs["end_address"]
    
    duration_diff = duration_in_traffic - duration
    if duration_diff < 0:
        traffic = "Low"
    elif duration_diff > 2:
        traffic = "High"
    else:
        traffic = "Medium"

    return distance, duration, duration_in_traffic, traffic, end_address


def get_weather(pickup_timestamp, end_address):
    # hämta ut stad från den valda adressen genom att splitta på ','
    # första elementet är address, andra elementet är stad, och sista är land (Kungsportsavenyen, Gothenburg, Sweden)
    # hämta då ut andra elementet och skicka in för att få väder för den valda staden
    city = end_address.split(", ")[1]
    city = city.split()[-1]

    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city},se&appid={WEATHER_API_KEY}&units=metric")
    
    data = response.json()

    # jämför alla datetimes i väder responsen med pickup_timestamp som användaren valt
    # och välj resultatet som är lägst(så nära 0 som möjligt)
    closest = min(data["list"], key=lambda x: abs(x["dt"] - pickup_timestamp))

    return closest["weather"][0]["main"]

