from turtle import update
from file_repository import FileRepository
from address_book_utils import AddressBookUtils
import json

utils = AddressBookUtils()

class AddressBookRepository(FileRepository):
    address_book = None

    def __init__(self) -> None:
        super().__init__("address.json")

    def get_address_book(self):
        if self.address_book == None:
            self.address_book = json.loads(super().readFile())
        return self.address_book

    def update(self, id, updateEntry):
        
        index = 0
        for entry in self.get_address_book():
            if entry.get("id") == id:
                break
            index += 1

        self.get_address_book()[index] = updateEntry
        self.save() 

    def save(self):
        super().writeFile(json.dumps(self.address_book, indent=4))
    
    def delete(self, id):
        index = 0
        for entry in self.get_address_book():
            if entry.get("id") == id:
                break

            index += 1

        self.get_address_book().pop(index)
        self.save()
        
    def search_entries(self, query):
        entries = []
        search_filter = lambda a, b: a.lower().find(b.lower()) != -1

        for entry in self.get_address_book():            
            if search_filter(entry.get("name"), query.lower()):
                entries.append(entry)
        return entries

    def add(self, entry):
        entry["id"] = utils.generate_id()
        self.get_address_book().append(entry)
        self.save()
