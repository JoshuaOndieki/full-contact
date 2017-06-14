import requests
import json

class FullContact():
    api_key = 'd6da175c32c576ec'
    url = "https://api.fullcontact.com/v2/person.json"

    def whois(api_key = api_key, url = url,**kwargs):
        kwargs['apiKey'] = api_key
        try:
            r = requests.get(url, params=kwargs)
            return r.json()
        except Exception:
            return "No Internet connection. Try Again!"
