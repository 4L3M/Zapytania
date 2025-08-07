import requests
import random

base_url = "http://localhost:3000"
token = "ee77de79-bc35-480e-856a-e1f7249e2c04"

# Przykładowe amerykańskie kody pocztowe
us_zip_codes = ["10001", "90210", "60601", "33101", "94105", "30301", "77001", "85001", "48201", "15201"]

def random_zip():
    return random.choice(us_zip_codes)

def random_street(n):
    return f"{n} Main St"

def random_time():
    return "09:00", "17:00"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

for i in range(1):

    customer_id = f"{i+1}"  # Zamień na faktyczne ID klientów!
    print(f"Adding addresses for customer ID: {customer_id}")
    url = f"{base_url}/api/customers/{customer_id}/address/create_multiple"
    addresses = []
    for j in range(5):
        time_from, time_to = random_time()
        address = {
            "country": "US",
            "name": f"Address{j+1}",
            "street": random_street(j+1),
            "zip_code": random_zip(),
            "working_all_day": False,
            "comments": "",
            "working_time_from": time_from,
            "working_time_to": time_to
        }
        addresses.append(address)
    response = requests.post(url, json=addresses, headers=headers)
    print(f"Customer {customer_id} - Status code:", response.status_code)
    print("Response:", response.text)