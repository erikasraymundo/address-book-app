import uuid


class AddressBookValidations():

    def validate_inputs(self, name, address, contact, email):
        def inputValidation(contact, email): return (
            email.find("@") > 0 or email == "")
        if name != "" and address != "":
            if inputValidation(contact, email):
                return True
            else:
                print(">> Error: Your contact number and/or email has invalid format.")
                return False
        else:
            print(">> Error: Name and address are required.")
            return False
