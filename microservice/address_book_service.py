from fastapi import FastAPI
from address_book_repository import AddressBookRepository
import json

app = FastAPI()
addressBookRepository = AddressBookRepository()

@app.get("/api/address-book/get-address-book")
def getAddressBook():
    return addressBookRepository.get_address_book()

@app.post("/api/address-book/add")
def add(entry: str):
    addressBookRepository.add(json.loads(entry))
    return json.dumps({"code": 200, "isSuccess": True})

@app.put("/api/address-book/update/{id}")
def update(id: str, entry: str):
    addressBookRepository.update(id, json.loads(entry))
    return json.dumps({"code": 200, "isSuccess": True})

@app.get("/api/address-book/search")
def search(name: str):
    return addressBookRepository.search_entries(name)

@app.delete("/api/address-book/delete/{id}")
def delete(id: str):
    return addressBookRepository.delete(id)