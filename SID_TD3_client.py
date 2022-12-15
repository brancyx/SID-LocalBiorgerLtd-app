#!/usr/bin/env python3
import requests as r  # import installed requests module
from requests.exceptions import HTTPError  # import requests exceptions
from requests.compat import urljoin  # could be usefull to create url…
import json


class Client:
    def __init__(self, baseUrl, defaultProtocol="http"):
        self.__baseUrl__ = baseUrl  # nom de domaine / Domain name
        self.__defaultProtocol__ = defaultProtocol  # Request protocol if not specified
        self.__r__ = None  # Server response
        self.__error__ = None  # errors

    # Changes the base url
    def set_baseurl(self, baseUrl):
        self.__baseUrl__ = baseUrl

    # Creates a url out of a Client object, a route and a protocol
    def make_url(self, route, protocol=None):
        if protocol == None:
            protocol = self.__defaultProtocol__
        baseurl = protocol + "://" + self.__baseUrl__
        url = urljoin(baseurl, route)
        return url  # Change in question 3

    # issues an http get request
    def get(self, route, payload={}, protocol=None):
        res = True
        try:
            # Stores in __r__ the response to the query
            self.__r__ = r.get(self.make_url(route, protocol), params=payload)
            print(self.__r__.url)
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        # possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    # issues an http get request
    def post(self, route, data=None, protocol=None):
        res = True
        try:
            # Stores in __r__ the response to the query
            if data == None:
                self.__r__ = r.post(self.make_url(route, protocol))
            else:
                self.__r__ = r.post(self.make_url(
                    route, protocol), json=json.dumps(data))
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        # possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    # returns the last response to a succesful query
    def lr(self):
        return self.__r__

    # returns the last error raised by a query
    def lr_error(self):
        return self.__error__

    def lr_status_code(self):
        res = None
        if self.__r__ != None:
            res = self.__r__.status_code  # Change in question 4
        return res

    def lr_headers(self):
        res = None
        if self.__r__ != None:
            res = self.__r__.headers  # Change in question 5
        return res

    def lr_response(self, json=False):
        res = None
        if self.__r__ != None:
            res = self.__r__  # Change in question 7
            if json:
                res = self.__r__.json()
        return res

    def lr_coordinates(self):
        res = None
        if self.__r__ != None:
            print(self.__r__)
            res = self.__r__.json()
            return res[0]["lat"], res[0]["lon"]
        return res

    def lr_closest_producer(self, top=5):
        res = None
        if self.__r__ != None:
            res = self.__r__.json()
            producer_list = res["items"][:top]
            updated_producer_list = []
            for producer in producer_list:
                coordinates = (producer["adressesOperateurs"][0]
                               ["lat"], producer["adressesOperateurs"][0]["long"])
                products = producer["productions"]
                siret = producer["siret"]
                producer_info = [siret, coordinates, products]
                updated_producer_list.append(producer_info)
            return updated_producer_list
        return res

    def lr_shortest_distance(self):
        res = None
        if self.__r__ != None:
            res = self.__r__.json()
            res = res["distance"]
        return res

    def lr_siret_company(self):
        res = None
        if self.__r__ != None:
            res = self.__r__.json()
            if len(res["results"]) > 0:  # Check if list is not empty
                res = res["results"][0]
            else:
                res = None
        return res


if __name__ == "__main__":
    print("START")
    # c = Client("127.0.0.1:5050/", "http")
    # payload = ["Banane", "Orange"]
    # if c.post("ingredients", data=payload):
    #     print(c.lr_status_code())
    #     print(c.lr_headers().get("Content-Type"))
    #     print(c.lr_response().text)
    # else:
    #     print(c.lr_error())

    # payload = {"city": "Lyon", "street": "Part Dieu"}
    # if c.post("location", data=payload):
    #     print(c.lr_status_code())
    #     print(c.lr_headers().get("Content-Type"))
    #     print(c.lr_response().text)
    # else:
    #     print(c.lr_error())

    # payload = "Pomme de terre"
    # if c.post("ingredients/Orange"):
    #     print(c.lr_status_code())
    #     print(c.lr_headers().get("Content-Type"))
    #     print(c.lr_response().text)
    # else:
    #     print(c.lr_error())

    # payload = {"city": "Lyon", "street": "Part Dieu"}
    # if c.post("location", data=payload):
    #     print(c.lr_status_code())
    #     print(c.lr_headers().get("Content-Type"))
    #     print(c.lr_response().text)
    # else:
    #     print(c.lr_error())

    # c = Client("nominatim.openstreetmap.org/", "https")
    # # Q15
    # # payload = {"addressdetails": "1",
    # #            "q": "pilkington+avenue,birmingham", "format": "json"}
    # # if c.get("", payload):
    # #     print(c.lr_status_code())
    # #     print(c.lr_headers().get("Content-Type"))
    # #     # print(c.lr_response().text)
    # #     print(c.lr_coordinates())  # (lat, lon)
    # # else:
    # #     print(c.lr_error())

    # # Q16
    # c.set_baseurl("opendata.agencebio.org/api/gouv/operateurs")
    # payload = {"activite": "Production", "produit": "Pommes de terre",
    #            "lat": "-21.065646", "lng": "55.279926"}
    # if c.get("", payload):
    #     print(c.lr_status_code())
    #     print(c.lr_headers().get("Content-Type"))
    #     producer_list = c.lr_closest_producer(3)
    #     print(len(producer_list))
    #     for producer in producer_list:
    #         print("Producer siret: ", producer[0])
    #         print("Producer coordinates: ", producer[1])
    #         print("Producer products: ", producer[2])
    #         print("\n")
    # else:
    #     print(c.lr_error())

    # # Q17
    # # c.set_baseurl("wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/")
    # # route?resource=bdtopo-osrm&start=2.337306%2C48.849319&end=2.367776%2C48.852891&profile=car&optimization=fastest&
    # # constraints=%7B%22constraintType%22%3A%22banned%22%2C%22key%22%3A%22wayType%22%2C%22operator%22%3A%22%3D%22%2C%22value%22%3A%22autoroute%22%7D&
    # # getSteps=true&getBbox=true&distanceUnit=kilometer&timeUnit=hour&crs=EPSG%3A4326
    # # 45.7825937,4.876612 45.6781458,4.5100394
    # # payload = {
    # #     "resource": "bdtopo-osrm", "start": "45.7825937,4.876612", "end": "45.6781458,4.5100394", "profile": "car",
    # #     "optimization": "fastest", "constraints": json.dumps({"constraintType": "banned", "key": "wayType", "operator": "=", "value": "autoroute"}),
    # #     "getSteps": 'true', "getBbox": 'true', "distanceUnit": "kilometer", "timeUnit": "hour", "crs": "EPSG:4326"
    # # }
    # # if c.get("route", payload):
    # #     print(c.lr_status_code())
    # #     print(c.lr_headers().get("Content-Type"))
    # #     print(c.lr_shortest_distance())
    # #     # https://wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start=2.337306%2C48.849319&end=2.367776%2C48.852891&profile=car&optimization=fastest&constraints=%7B%22constraintType%22%3A%22banned%22%2C%22key%22%3A%22wayType%22%2C%22operator%22%3A%22%3D%22%2C%22value%22%3A%22autoroute%22%7D&getSteps=true&getBbox=true&distanceUnit=kilometer&timeUnit=hour&crs=EPSG%3A4326
    # #     # https://wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start=2.337306%2C48.849319&end=2.367776%2C48.852891&profile=car&optimization=fastest&constraints=constraintType&constraints=key&constraints=operator&constraints=value&getSteps=true&getBbox=true&distanceUnit=kilometer&timeUnit=hour&crs=EPSG%3A4326
    # # else:
    # #     print(c.lr_error())

    # # Q18
    # # c.set_baseurl("recherche-entreprises.api.gouv.fr")
    # # payload = {"q": "35600000000048"}
    # # if c.get("search", payload):
    # #     print(c.lr_status_code())
    # #     print(c.lr_headers().get("Content-Type"))
    # #     print(c.lr_siret_company())
    # # else:
    # #     print(c.lr_error())

    # # Q19
    # Get coordinates of postal code
    # payload = {"addressdetails": "1", "q": "69621", "format": "json"}
    # coordinates = (0, 0)  # default
    # if c.get("", payload):
    #     coordinates = c.lr_coordinates()
    #     print(coordinates)  # (lat, lon)
    # else:
    #     print(c.lr_error())

    # # Get list of producers and list of products (save coordinates, siret_number)
    # c.set_baseurl("opendata.agencebio.org/api/gouv/operateurs")
    # payload = {"activite": "Production",
    #            "lat": coordinates[0], "lng": coordinates[1]}
    # producer_list = []
    # if c.get("", payload):
    #     producer_list = c.lr_closest_producer(3)
    #     print(len(producer_list))
    # else:
    #     print(c.lr_error())

    # # Get driving distance
    # c.set_baseurl("wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/")
    # coordinates_str = str(coordinates[0]) + "," + str(coordinates[1])
    # for producer in producer_list:
    #     prod_coordinates = str(producer[1][0]) + "," + str(producer[1][1])
    #     print(coordinates_str, prod_coordinates)
    #     payload = {
    #         "resource": "bdtopo-osrm", "start": coordinates_str, "end": prod_coordinates, "profile": "car",
    #         "optimization": "fastest", "constraints": json.dumps({"constraintType": "banned", "key": "wayType", "operator": "=", "value": "autoroute"}),
    #         "getSteps": 'true', "getBbox": 'true', "distanceUnit": "kilometer", "timeUnit": "hour", "crs": "EPSG:4326"
    #     }
    #     if c.get("route", payload):
    #         # print(c.lr_status_code())
    #         # print(c.lr_headers().get("Content-Type"))
    #         dist = c.lr_shortest_distance()
    #         print("DISTANCE: ", dist)
    #         # https://wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start=2.337306%2C48.849319&end=2.367776%2C48.852891&profile=car&optimization=fastest&constraints=%7B%22constraintType%22%3A%22banned%22%2C%22key%22%3A%22wayType%22%2C%22operator%22%3A%22%3D%22%2C%22value%22%3A%22autoroute%22%7D&getSteps=true&getBbox=true&distanceUnit=kilometer&timeUnit=hour&crs=EPSG%3A4326
    #         # https://wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start=2.337306%2C48.849319&end=2.367776%2C48.852891&profile=car&optimization=fastest&constraints=constraintType&constraints=key&constraints=operator&constraints=value&getSteps=true&getBbox=true&distanceUnit=kilometer&timeUnit=hour&crs=EPSG%3A4326
    #     else:
    #         print(c.lr_error())

    # # Get first and last name of manager (using lr_siret_company)
    # c.set_baseurl("recherche-entreprises.api.gouv.fr")
    # for producer in producer_list:
    #     siret_str = str(producer[0])
    #     payload = {"q": siret_str}
    #     if c.get("search", payload):
    #         print(c.lr_status_code())
    #         print(c.lr_headers().get("Content-Type"))
    #         output = c.lr_siret_company()
    #         if output:
    #             leader_name = (output["dirigeants"][0]["nom"],
    #                            output["dirigeants"][0]["prenoms"])
    #             producer.append(leader_name)
    #         else:
    #             producer.append(None)
    #     else:
    #         print(c.lr_error())
