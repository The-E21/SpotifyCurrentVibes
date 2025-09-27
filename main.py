from backend import backend
import json

be = backend()
be.refresh()

results = be.get_recently_listened_to()
for idx, item in enumerate(results):
    track = item
    print(idx, track['id'], " – ", track['name'])