import requests
from enum import StrEnum

API_URL = 'https://photon.komoot.io/api/'
QUERY_KEY = 'q'
LANGUAGE_KEY = 'lang'
LIMIT_KEY = 'limit'
    
def search_by_term(params):
    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.text}")
    return response.json()

def simplify_json(raw_response):
    results = []
    for feature in raw_response["features"]:
        point = Location()

        point.city = feature["properties"]["city"] if "city" in feature["properties"] else None
        point.state = feature["properties"]["state"] if "state" in feature["properties"] else None
        point.country = feature["properties"]["country"] if "country" in feature["properties"] else None
        point.name = feature["properties"]["name"] if "name" in feature["properties"] else None
        point.latitude = feature["geometry"]["coordinates"][1]
        point.longitude = feature["geometry"]["coordinates"][0]
        
        results.append(point)
    return results

class ApiOptions():
    def __init__(self):
        self.language = Language.EN
        self.limit = 1
    
    def get_params(self):
        dictionary = {}
        dictionary[LANGUAGE_KEY] = str(self.language)
        dictionary[LIMIT_KEY] = self.limit
        return dictionary

class Language(StrEnum):
    Default = "default"
    EN = "en"
    FR = "fr"
    DE = "de"

class Geolocator():
    def __init__(self):
        self.options = ApiOptions()

    def search(self, search_term: str):
        params = self.options.get_params()
        params[QUERY_KEY] = search_term
        return simplify_json(search_by_term(params))

class Location:
    def __init__(self):
        self.name = ""
        self.city = ""
        self.state = ""
        self.country = ""
        self.latitude = 0.0
        self.longitude = 0.0