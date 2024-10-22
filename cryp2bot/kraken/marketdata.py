import requests


def ticker(parameter):

    url = "https://api.kraken.com/0/public/Ticker?pair=" + parameter

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
