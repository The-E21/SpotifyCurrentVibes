from backend import backend
import authenticator

auth_data = authenticator.read_auth_data()
be = backend(auth_data["client_id"], auth_data["client_secret"], auth_data["redirect_uri"])
be.refresh()

results = be.get_recently_listened_to()
for idx, item in enumerate(results):
    track = item
    print(idx, track['id'], " – ", track['name'])