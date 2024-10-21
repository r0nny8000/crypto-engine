import requests


def server_time():
    """Get the server's time."""
    url = "https://api.kraken.com/0/public/Time"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print("Server time: ", response.text)
