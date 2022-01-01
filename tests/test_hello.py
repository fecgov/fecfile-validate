import requests

def get_hello():
    r = requests.get('http://localhost:5000/')
    # return r.json
    return r.text

def ztest_hello():
    assert get_hello() == "Hello, World!"