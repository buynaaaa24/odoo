import json
import random
import urllib.request

url = 'http://localhost:8017/'  # Correct variable name
username = 'admin'
password = 'admin'
db = 'odoo17_b'


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000)
    }
    headers = {
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers=headers)

    response = json.loads(urllib.request.urlopen(req).read().decode("UTF-8"))

    if response.get('error'):
        raise Exception(response["error"])
    return response["result"]


def call(url, service, method, *args):
    return json_rpc(f"{url}/jsonrpc", "call", {"service": service, "method": method, "args": args})


# Authenticate user
user_id = call(url, "common", "login", db, username, password)

print("User ID:", user_id)

# Fetch available fields in the estate.property model
fields = call(url, "object", "execute", db, user_id, password, 'estate.property', 'fields_get', [], {'attributes': ['string', 'type', 'required']})

# Print available fields for debugging
print("Available fields in 'estate.property':")
print(json.dumps(fields, indent=4))

# Create a new property with valid fields
# For demonstration, only using the 'name' field, modify as needed based on available fields
vals = {
    "name": "Property from JSON"
}

# create_property = call(url, "object", "execute", db, user_id, password, 'estate.property', 'create', vals)
# print("Created property ID:", create_property)

read_property = call(url, "object", "execute", db, user_id, password, 'estate.property', 'read', [19])
print(read_property)
