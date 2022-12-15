#!/usr/bin/env python3
from SID_TD3_client import Client
import json


class OSM_Client(Client):
    def __init__(self):
        super().__init__("nominatim.openstreetmap.org", "https")

    def get_coordinates(self, location):
        res = False
        payload = {"addressdetails": "1",
                   "q": location, "format": "json"}
        if self.get("", payload) and self.lr_status_code() == 200:
            response = self.lr_response(True)
            if len(response) > 0:
                res = {}
                res["lat"] = response[0]['lat']
                res["lng"] = response[0]['lon']
        else:
            print(self.lr().url, self.lr_error())
        return res


class BIO_Client(Client):
    def __init__(self):
        super().__init__("opendata.agencebio.org/api/gouv/operateurs", "https")

    def get_producer_list(self, lat, long, ingredient):
        res = False
        payload = {"activite": "Production", "produit": ingredient,
                   "lat": lat, "lng": long}
        if self.get("", payload) and self.lr_status_code() == 200:
            response = self.lr_response(True)
            res = {}
            res["producers"] = response["items"][:5]
        else:
            print(self.lr().url, self.lr_error())
        return res


class IGN_Client(Client):
    def __init__(self):
        super().__init__("wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/", "https")

    def get_driving_distance(self, start_coord, end_coord):
        res = False
        payload = {
            "resource": "bdtopo-osrm", "start": start_coord, "end": end_coord, "profile": "car",
            "optimization": "fastest", "constraints": json.dumps({"constraintType": "banned", "key": "wayType", "operator": "=", "value": "autoroute"}),
            "getSteps": 'true', "getBbox": 'true', "distanceUnit": "kilometer", "timeUnit": "hour", "crs": "EPSG:4326"
        }
        if self.get("route", payload) and self.lr_status_code() == 200:
            response = self.lr_response(True)
            res = {}
            res["distance"] = response["distance"]
        else:
            print(self.lr().url, self.lr_error())
        return res


class GOV_Client(Client):
    def __init__(self):
        super().__init__("recherche-entreprises.api.gouv.fr", "https")

    def get_company_info(self, siret_str):
        res = False
        payload = {"q": siret_str}
        if self.get("search", payload) and self.lr_status_code() == 200:
            response = self.lr_response(True)
            res = {}
            print("\n\n")
            print(response["results"])
            print("\n\n")
            if len(response["results"]) > 0:
                res["nom"] = response["results"][0]["dirigeants"][0]["nom"]
                res["prenom"] = response["results"][0]["dirigeants"][0]["prenoms"]
            else:
                res["nom"] = None
                res["prenom"] = None
        else:
            print(self.lr().url, self.lr_error())
        return res
