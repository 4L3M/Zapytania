import random
from datetime import date, timedelta
import requests
import json

url = "http://localhost:3000/api/orders/order/create"
token = "ee77de79-bc35-480e-856a-e1f7249e2c04"

def random_august_date():
    day = random.randint(1, 31)
    return date(2025, 8, day)

def random_delivery_date(pickup_dt):
    # delivery is pickup + [3, 5] days
    add_days = random.randint(3, 5)
    return pickup_dt + timedelta(days=add_days)

def correlated_weight(pallet_spots):
    # base: 1200kg per spot ± 40%
    base = pallet_spots * 1200
    variation = base * random.uniform(-0.4, 0.5)
    weight = max(0, int(base + variation))
    # allow some outliers
    if random.random() < 0.1:
        weight += random.randint(-5000, 5000)
    weight = max(1000, weight)  # Ensure weight is not negative
    weight = min(weight, 40000)  # Cap weight to a maximum of 50,000 kg
    return weight


headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

orders = []
for _ in range(50):
    origin_billing_id = random.randint(2, 51)
    # destination id: different & at least 5 apart
    offset = random.choice([i for i in range(5, 50) if origin_billing_id + i <= 51 or origin_billing_id - i >= 2])
    if origin_billing_id + offset <= 51:
        destination_id = origin_billing_id + offset
    else:
        destination_id = origin_billing_id - offset

    rate_amount = random.randint(0, 2000)
    pickup_dt = random_august_date()
    delivery_dt = random_delivery_date(pickup_dt)

    pallet_spots = random.randint(0, 30)
    total_weight = correlated_weight(pallet_spots)
    order = {
        "origin_address_id": origin_billing_id,
        "billing_address_id": origin_billing_id,
        "destination_address_id": destination_id,
        "status": "BOO",
        "rate_amount": rate_amount,
        "pickup_date": pickup_dt.isoformat(),
        "pickup_time_from":"00:00",
        "pickup_time_to": "23:59",
        "pickup_all_day": False,
        "delivery_date": delivery_dt.isoformat(),
        "delivery_time_from": "00:00",
        "delivery_time_to": "23:59",
        "delivery_all_day": False,
        "group_id": 1,
        "delivery_preference": "R",
        "is_splittable": random.choice([True, False]),
        "delivered_as_one": False,
        "is_consolidated": False,
        "is_archived": False,
        "hub_id": 1,
        "actual_number_of_pallet_spots": pallet_spots,
        "container_type": "B",
        "actual_total_weight": total_weight,
        "customer_reference_number": "",
        "total_length": round(pallet_spots * 1.75, 2),
        "total_weight": total_weight,
        "pallet_length": 1.75,
        "required_temperature": None,
        "origin_contact_id": None,
        "billing_contact_id": None,
        "destination_contact_id": None,
        "description": "",
        "delivery_number": "",
        "pickup_number": "",
        "purchase_order_number": "",
        "delivery_contact": "",
        "internal_number": "1",
        "internal_shippment_number": "1",
        "internal_trailer_number": "1",
        "spots": pallet_spots
    }
    orders.append(order)
for order in orders:
    print("Order:", json.dumps(order, indent=2))
    response = requests.post(url, json=order, headers=headers)
    print("Status code:", response.status_code)
    print(response.text)