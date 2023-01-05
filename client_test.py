from SID_TD3_client import Client


class ClientTest(Client):
    def __init__(self, host="localhost", port=5000):
        super().__init__(f"{host}:{port}/", "http")
        print(self.__baseUrl__)

    def test_route_owners(self):
        test_data = ["newmember1", "newmember1", "newmember2"]
        for i in range(3):
            self.post(f"owners/{test_data[i]}")
            if i == 1 and self.lr_status_code() == 304:
                print(i, self.lr_status_code(), "OK")
            elif self.lr_status_code() == 200:
                print(i, self.lr_status_code(), "OK")
            else:
                print(i, self.lr_status_code(), "Problem")

    def test_route_producers(self):  # TODO
        if self.get("producers"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    def test_route_get_ingredients(self):
        if self.get("ingredients"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    def test_route_post_ingredients(self):
        payload = ["Banane", "Orange"]  # TODO
        if self.post("ingredients", data=payload):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    def test_route_add_ingredients(self, ingred):
        if self.post(f"ingredients/{ingred}"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    def test_route_delete_all_ingredients(self):
        if self.delete(f"ingredients"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    def test_route_del_ingredient(self, ingred):
        if self.delete(f"ingredients/{ingred}"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    def test_route_add_location(self, city, street):
        payload = {"city": city, "street": street}
        if self.post(f"location", data=payload):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    def test_route_get_location(self):
        if self.get(f"location"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())


if __name__ == "__main__":
    c = ClientTest(port=5050)
    c.test_route_post_ingredients()
    # c.test_route_get_ingredients()
    c.test_route_add_ingredients("Pommes de terre")
    # c.test_route_add_ingredients("Banane")
    # c.test_route_delete_all_ingredients()
    # c.test_route_get_ingredients()
    # c.test_route_del_ingredient("Lemon")  # 200 del: ingred found
    # c.test_route_del_ingredient("Apple")  # 304 del: ingred not found
    c.test_route_add_location("Rennes", "5, allee Geoffroy de Pontblanc")
    c.test_route_producers()
