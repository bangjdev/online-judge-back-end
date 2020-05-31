import json


def create_message(message_code="", results={}):
    data = {
    	'message_code': message_code,
        'results': results
    }
    return data
