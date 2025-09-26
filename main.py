import backend

be = backend.backend()
results = be.get_recently_listened_to()
for idx, item in enumerate(results):
    print(idx, item['artists'][0]['name'], " – ", item['name'], "-", item["id"])
