from requests import request
from http_repository import HttpRepository
import json

class AddressBookApiClient(HttpRepository):

    def __init__(self) -> None:
        super().__init__("http://127.0.0.1:8000/api/address-book")

    def get_address_book(self):
        return json.loads(super().do_get("/get-address-book"))

    def add_new_address_book(self, entry):
        request = {"entry": json.dumps(entry)}
        return super().do_post("/add", request_params=request)

    def update_entry(self, id, entry):
        request = {"entry": json.dumps(entry)}
        return super().do_put("/update/{}".format(id), request_params=request)

    def delete_entry(self, id):
        return super().do_delete("/delete/{}".format(id))

    def search_entries(self, query):
        return json.loads(super().do_get("/search?name={}".format(query)))

