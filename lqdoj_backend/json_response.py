import json


def create_message(code, results={}):
    data = {
    	'message_code': code,
        'results': results
    }
    return data
