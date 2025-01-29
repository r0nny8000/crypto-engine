import os
from kraken.spot import User

def get_balance():
    """
    Fetches and prints the account balance from Kraken.

    This function authenticates the user using API key and secret from environment variables,
    then retrieves and prints the account balance and the balance for a specific currency (EUR).
    """
    user = User(
        key=os.getenv('KRAKEN_API_KEY'),
        secret=os.getenv('KRAKEN_API_SECRET')) # authenticated

    print(user.get_account_balance())
    print(user.get_balance(currency="EUR"))
