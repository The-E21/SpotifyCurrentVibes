import json

AUTH_DATA_FILE_NAME = "auth_data.json"

def write_auth_data(client_id, client_secret, redirect_uri):
    data = {"client_id" : client_id, "client_secret" : client_secret, "redirect_uri" : redirect_uri}
    json_str = json.dumps(data, indent=4)
    with open(AUTH_DATA_FILE_NAME, "w") as file:
        file.write(json_str)

def read_auth_data() -> dict:
    with open(AUTH_DATA_FILE_NAME, "r") as file:
        return json.load(file)