import pytest
import requests

def test_url_malware_200():
    res = requests.get("http://127.0.0.1:5000/v1/urlinfo/https://www.w3schools.com/")
    assert res.status_code == 200
    assert res.json() == {"message": "Access Allowed, NOT a Malware URL",
                            "safe": True}

def test_url_malware_403():
    res = requests.get("http://127.0.0.1:5000/v1/urlinfo/https://th-track-thailandpost.com/business/solutions/products/standard")
    assert res.status_code == 403
    assert res.json() == {"message": "Error: Malware URL",
                            "safe": False}

def test_malformed_url_with_http_400():
    res = requests.get("http://127.0.0.1:5000/v1/urlinfo/https://www.caet-org.com/secure/citibank.com.th/online%20upd")
    assert res.status_code == 400
    assert res.json() == {"message": "Bad Request Error, check the URL",
                            "safe": False}

def test_malformed_url_without_http_400():
    res = requests.get("http://127.0.0.1:5000/v1/urlinfo/tiny.com")
    assert res.status_code == 400
    assert res.json() == {"message": "Bad Request Error, check the URL",
                            "safe": False}

def test_delete_malware_url():
    res = requests.get("http://127.0.0.1:5000/delete/https://www.caet-org.com/secure/citibank.com.th/online%20upd")
    assert res.status_code == 200
    assert res.json() == {"message": "Deleted"}


