from base_client import Client


class ClientTest(Client):
    def __init__(self, host="localhost", port=5000):
        super().__init__(f"{host}:{port}/", "http")
        print(self.__baseUrl__)

    # Test post request of owners
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

    # Test get request of producers
    def test_route_producers(self):
        if self.get("producers"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    # Test get request of all ingredients
    def test_route_get_ingredients(self):
        if self.get("ingredients"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    # Test post request of entire ingredient list (replace)
    def test_route_post_ingredients(self, ingredient_list):
        if self.post("ingredients", data=ingredient_list):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    # Test post request of individual ingredient (append)
    def test_route_add_ingredients(self, ingred):
        if self.post(f"ingredients/{ingred}"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    # Test delete request of entire ingredient list
    def test_route_delete_all_ingredients(self):
        if self.delete(f"ingredients"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    # Test delete request of individual ingredient
    def test_route_del_ingredient(self, ingred):
        if self.delete(f"ingredients/{ingred}"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    # Test post request of location
    def test_route_add_location(self, city, street):
        payload = {"city": city, "street": street}
        if self.post(f"location", data=payload):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())

    # Test get request of location
    def test_route_get_location(self):
        if self.get(f"location"):
            print(self.lr_status_code())
            print(self.lr_headers().get("Content-Type"))
            print(self.lr_response().text)
        else:
            print(self.lr_error())


if __name__ == "__main__":
    c = ClientTest(port=5050)

    # Test 1.1 /ingredients routes
    print("\nTest 1.1:")
    ingredient_list = ["Banane, Orange"]
    c.test_route_post_ingredients(ingredient_list)
    c.test_route_get_ingredients()
    c.test_route_delete_all_ingredients()

    # Test 1.2 /ingredients/<ing> routes
    print("\nTest 1.2:")
    c.test_route_add_ingredients("Pommes de terre")  # 200: Success
    c.test_route_add_ingredients("Lemon")  # 200: Success
    c.test_route_add_ingredients("Banane")  # 200: Success
    c.test_route_add_ingredients("Banane")  # 304: No change
    c.test_route_del_ingredient("Lemon")  # 200 del: Success
    c.test_route_del_ingredient("Apple")  # 304 del: No change

    # Test 1.3 /location route
    print("\nTest 1.3:")
    c.test_route_add_location("Lyon", "INSA Einstein Road")  # 200: Success
    c.test_route_add_location(
        "Rennes", "5, allee Geoffroy de Pontblanc")  # 200: Success
    c.test_route_get_location()

    # Test 1.4 /producers route
    print("\nTest 1.4:")
    c.test_route_producers()  # 200: Success
    c.test_route_delete_all_ingredients()
    c.test_route_producers()  # 400: ["ingredients"]
