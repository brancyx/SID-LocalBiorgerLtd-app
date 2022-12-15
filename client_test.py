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

    def test_route_producers(self):
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
        payload = ["Banane", "Orange"]
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


if __name__ == "__main__":
    c = ClientTest(port=5050)
    c.test_route_producers()
    # c.test_route_post_ingredients()
    # c.test_route_get_ingredients()
    # c.test_route_add_ingredients("Lemon")
