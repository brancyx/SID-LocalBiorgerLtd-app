#!/usr/bin/env python3
import mimetypes
from flask import Flask  # server
from flask import request  # to handle the different http requests
# to reply (we could use jsonify as well but we handled it)
from flask import Response
import json
from SID_TD3_client import Client
from OSM_client import OSM_Client, BIO_Client, IGN_Client, GOV_Client
import time


class LocalBiorger:
    def __init__(self):
        self.owners = {}
        self.owners["127.0.0.1"] = ["test1", "test2", "test3"]  # question4
        self.ingredients = {}
        self.location = {}

    # Regarde si l'adresse ip est référencée, sinon crée une liste vide
    def check_ip(self, client_ip):
        if client_ip not in self.owners.keys():
            self.owners[client_ip] = []
        if client_ip not in self.ingredients.keys():
            self.ingredients[client_ip] = []
        if client_ip not in self.location.keys():
            self.location[client_ip] = {}

    # Renvoie les développeurs associés à l'adresse ip (en json ou non)
    def get_owners(self, ip, injson=False):
        if injson:
            res = json.dumps(self.owners[ip])
        else:
            res = self.owners[ip]
        return res

    # ajoute un propriétaire à la liste des clients associés à l'adresse ip
    def add_owner(self, ip, owner):
        res = False
        if owner not in self.owners[ip]:
            self.owners[ip].append(owner)
            res = self.owners[ip]
        return res

    def add_ingred(self, ip, ingred):
        res = False
        if ingred not in self.ingredients[ip]:
            self.ingredients[ip].append(ingred)
            res = self.ingredients[ip]
        return res

    def get_ingredients(self, ip, injson=False):
        if injson:
            res = json.dumps(self.ingredients[ip])
        else:
            res = self.ingredients[ip]
        return res

    def get_closest_producer(self, location, ingredient):
        osm = OSM_Client()
        bio = BIO_Client()
        ign = IGN_Client()
        gov = GOV_Client()
        coord = osm.get_coordinates(location)
        raw_producer_list = bio.get_producer_list(
            coord["lat"], coord["lng"], ingredient)

        if raw_producer_list["producers"] == []:
            return {"Error": "No producers found"}

        closest_prod = raw_producer_list["producers"][0]
        info = {}
        user_coord = str(coord["lng"]) + "," + str(coord["lat"])
        prod_coord = str(closest_prod["adressesOperateurs"][0]["long"]) + \
            "," + str(closest_prod["adressesOperateurs"][0]["lat"])
        distance = ign.get_driving_distance(user_coord, prod_coord)
        enterprise_nom = closest_prod["denominationcourante"]
        # leader_info = gov.get_company_info(closest_prod["siret"])
        manager_nom = closest_prod["gerant"]

        if enterprise_nom:
            info["Enterprise"] = enterprise_nom
        else:
            info["Enterprise"] = "Unknown"

        info["coord"] = str(closest_prod["adressesOperateurs"][0]["lat"]) + \
            "," + str(closest_prod["adressesOperateurs"][0]["long"])
        info["Distance(km)"] = distance["distance"]

        if manager_nom:
            info["Manager"] = manager_nom
        else:
            info["Manager"] = "Unknown"

        # if leader_info:
        #     info["leader_nom"] = leader_info['nom']
        #     info["leader_prenom"] = leader_info['prenom']
        # else:
        #     info["leader_nom"] = "Unknown"
        #     info["leader_prenom"] = "Unknown"
        return info

    def del_ingred(self, ip, ingred):
        res = False
        if ingred in self.ingredients[ip]:
            self.ingredients[ip].remove(ingred)
            res = self.ingredients[ip]
        return res


# On crée le serveur
app = Flask(__name__)

# On crée l'objet qui va gérer les données
LB_ltd = LocalBiorger()

# Route de test, va afficher l'adresse IP


@app.route('/', methods=['GET'])
def index():
    ip = request.remote_addr
    response = f"<p>Server is running, your ip is {ip}</p>"
    return Response(response, status=200)  # Question2


# /ingredients [POST, GET, DELETE]


@app.route('/ingredients', methods=['POST', 'GET', 'DELETE'])
def set_ingredient_list():
    ip = request.remote_addr
    LB_ltd.check_ip(ip)
    if request.method == "GET":
        ingredient_list = LB_ltd.ingredients[ip]
        res = json.dumps(ingredient_list)
        response = f"Ingredient list: {res}"
        return Response(res, status=200)
    elif request.method == "POST":
        if request.is_json:
            LB_ltd.ingredients[ip] = json.loads(request.get_json())
        ingredient_list = LB_ltd.ingredients[ip]
        res = json.dumps(ingredient_list)
        response = f"Ingredient list: {res}"
        return Response(response, status=200)
    elif request.method == "DELETE":
        LB_ltd.ingredients[ip] = []
        response = f"Delete successful"
        return Response(response, status=200)

# /ingredients/<ingred> POST


@app.route('/ingredients/<ingred>', methods=['POST'])
def add_ingredients(ingred):
    ip = request.remote_addr
    LB_ltd.check_ip(ip)
    r = LB_ltd.add_ingred(ip, ingred)
    if r == False:
        resp = Response(LB_ltd.get_ingredients(ip, True), status=304,
                        mimetype="application/json")  # question4
    else:
        resp = Response(LB_ltd.get_ingredients(ip, True), status=200,
                        mimetype="application/json")  # question4
    print(resp)
    return resp


# /location ['POST', 'GET']

@app.route('/location', methods=['POST', 'GET'])
def location():
    ip = request.remote_addr
    LB_ltd.check_ip(ip)
    if request.method == "GET":
        location = LB_ltd.location[ip]
        res = json.dumps(location)
        response = f"Location: {res}"
        return Response(res, status=200)
    elif request.method == "POST":
        if request.is_json:
            LB_ltd.location[ip] = json.loads(request.get_json())
        location = LB_ltd.location[ip]
        res = json.dumps(location)
        response = f"location: {res}"
        return Response(response, status=200)


# /producers GET
@app.route('/producers', methods=['GET'])
def get_producers():
    ip = request.remote_addr
    LB_ltd.check_ip(ip)
    status = None
    if LB_ltd.location[ip] == {} and LB_ltd.ingredients[ip] == []:
        res = ["location", "ingredients"]
        status = 400
    elif LB_ltd.location[ip] == {}:
        res = ["location"]
        status = 400
    elif LB_ltd.ingredients[ip] == []:
        res = ["ingredients"]
        status = 400
    else:
        location = LB_ltd.location[ip]["street"] + \
            "," + LB_ltd.location[ip]["city"]
        ingredients = LB_ltd.ingredients[ip]
        res = {}
        for ing in ingredients:
            producers = LB_ltd.get_closest_producer(location, ing)
            res[ing] = producers
        status = 200
    res = json.dumps(res)
    return Response(res, status=status)

# /ingredients/<ingred> DELETE


@app.route('/ingredients/<ingred>', methods=['DELETE'])
def delete_ingredients(ingred):
    ip = request.remote_addr
    LB_ltd.check_ip(ip)
    r = LB_ltd.del_ingred(ip, ingred)
    if r == False:
        resp = Response(LB_ltd.get_ingredients(ip, True), status=304,
                        mimetype="application/json")
    else:
        resp = Response(LB_ltd.get_ingredients(ip, True), status=200,
                        mimetype="application/json")
    return resp

# /declare/<ip> POST #TODO
# Liste les propriétaires associés à l'adresse IP qui interroge la ressource


@app.route('/owners', methods=['GET'])
def list_owners():
    ip = request.remote_addr
    LB_ltd.check_ip(ip)  # Si l'IP n'existe pas on la crée
    res = LB_ltd.get_owners(ip, True)
    return Response(res, status=200, mimetype="application/json")  # question3

# Ajoute un membre associé à l'adresse IP qui interroge la ressource


@app.route('/owners/<membre>', methods=['POST', 'GET'])
def add_owner(membre):
    ip = request.remote_addr
    LB_ltd.check_ip(ip)  # Si l'IP n'existe pas on la crée
    # TODO ajouter un membre à la liste LB_Ltd
    r = LB_ltd.add_owner(ip, membre)
    if r == False:
        resp = Response(LB_ltd.get_owners(ip, True), status=304,
                        mimetype="application/json")  # question4
    else:
        resp = Response(LB_ltd.get_owners(ip, True), status=200,
                        mimetype="application/json")  # question4
    return resp


# will only execute if this file is run
if __name__ == "__main__":
    debugging = True
    # lance le serveur (port par défaut 5000, à utiliser pour votre serveur)
    app.run(host="0.0.0.0", port="5050", debug=debugging)
