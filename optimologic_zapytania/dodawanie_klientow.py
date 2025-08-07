import requests

url = "http://localhost:3000/api/customers/customer/create_multiple"
token = "ee77de79-bc35-480e-856a-e1f7249e2c04"

payload = [
    {"name": f"company{i+1}", "comments": ""}
    for i in range(10)
]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status code:", response.status_code)
print("Response:", response.text)