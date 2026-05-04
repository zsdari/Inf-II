import requests

url = "http://127.0.0.1:23456"  # vagy 8000, ha azon fut
parameter = {'name': 'Adam', 'age': 30}

response = requests.get(url, params=parameter)

print("Status Code:", response.status_code)
print("Answer JSON:", response.json())