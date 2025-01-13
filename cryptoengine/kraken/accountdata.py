import os
from kraken.spot import User



print(os.getenv('KRAKEN_API_KEY'))
print(os.getenv('KRAKEN_API_SIGN'))



user = User(key=os.getenv('KRAKEN_API_KEY'), secret=os.getenv('KRAKEN_API_SIGN')) # authenticated
print(user.get_account_balance())
print(user.get_balance(currency="EUR"))
