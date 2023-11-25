import re

def validate_name(name):
    if re.match("^[A-Za-z ]+$", name):
        return True
    return False

def validate_address(address):
    if address:
        return True
    return False
