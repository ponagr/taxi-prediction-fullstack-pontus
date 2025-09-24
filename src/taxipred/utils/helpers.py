import requests 
from urllib.parse import urljoin

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