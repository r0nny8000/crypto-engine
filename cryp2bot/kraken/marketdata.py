import requests
import json

def price(pairs):

    
    url = "https://api.kraken.com/0/public/Ticker?pair=" + pairs

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=4).json()
    
    if 'result' not in response:
        return None
    
    print(json.dumps(response, indent=4))
    
    key = list(response['result'].keys())[0]
    
    bid_price = response['result'][key]['b'][0]
    print(f"The bid price for {pairs} is {bid_price}")

    prices = {}

    prices[key] = bid_price
    return prices
