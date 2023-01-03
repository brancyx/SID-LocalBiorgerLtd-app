#!/usr/bin/env python3
import mimetypes
from flask import Flask  # server
from flask import request  # to handle the different http requests
# to reply (we could use jsonify as well but we handled it)
from flask import Response
import json
from SID_TD3_client import Client
from OSM_client import OSM_Client, BIO_Client, IGN_Client, GOV_Client


class LocalBiorger:
    def __init__(self):
        self.owners = {}
        self.owners["127.0.0.1"] = ["test1", "test2", "test3"]  # question4
        self.ingredients = {}
        # self.ingredients["127.0.0.1"] = []  # ["Pommes de terre", "Pain frais"]
        self.location = {}
        self.location["127.0.0.1"] = {
            "city": "Villeurbane", "street": "Einstein Avenue"}

    # Regarde si l'adresse ip est référencée, sinon crée une liste vide
    def check_ip(self, client_ip):
        if client_ip not in self.owners.keys():
            self.owners[client_ip] = []
        if client_ip not in self.ingredients.keys():
            self.ingredients[client_ip] = []

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

    def get_producers(self, location, ingredient):
        osm = OSM_Client()
        bio = BIO_Client()
        ign = IGN_Client()
        gov = GOV_Client()
        coord = osm.get_coordinates(location)
        raw_producer_list = bio.get_producer_list(
            coord["lat"], coord["lng"], ingredient)

        producer_list = {}
        producer_list["producers"] = []

        for producer in raw_producer_list["producers"]:
            info = {}
            user_coord = str(coord["lat"]) + "," + str(coord["lng"])
            prod_coord = str(producer["adressesOperateurs"][0]["lat"]) + \
                "," + str(producer["adressesOperateurs"][0]["long"])
            distance = ign.get_driving_distance(user_coord, prod_coord)
            leader_info = gov.get_company_info(producer["siret"])
            info["coord"] = prod_coord
            info["distance(km)"] = distance["distance"]
            info["leader_nom"] = leader_info['nom']
            info["leader_prenom"] = leader_info['prenom']
            producer_list["producers"].append(info)

        return producer_list

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
        response = f"<p>Ingredient list: {res}</p>"
        return Response(res, status=200)
    elif request.method == "POST":
        if request.is_json:
            LB_ltd.ingredients[ip] = json.loads(request.get_json())
        ingredient_list = LB_ltd.ingredients[ip]
        res = json.dumps(ingredient_list)
        response = f"<p>Ingredient list: {res}</p>"
        return Response(response, status=200)
    elif request.method == "DELETE":
        LB_ltd.ingredients[ip] = []
        response = f"<p>Delete successful</p>"
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
        response = f"<p>Location: {res}</p>"
        return Response(res, status=200)
    elif request.method == "POST":
        if request.is_json:
            print("success")
            LB_ltd.location[ip] = json.loads(request.get_json())
        location = LB_ltd.location[ip]
        res = json.dumps(location)
        response = f"<p>location: {res}</p>"
        return Response(response, status=200)


# /producers GET
@app.route('/producers', methods=['GET'])
def get_producers():
    res = LB_ltd.get_producers("69621", "Pommes de terre")
    return res

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

# /declare/<ip> POST
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
    print(resp)
    return resp


# will only execute if this file is run
if __name__ == "__main__":
    debugging = True
    # lance le serveur (port par défaut 5000, à utiliser pour votre serveur)
    app.run(host="0.0.0.0", port="5050", debug=debugging)
