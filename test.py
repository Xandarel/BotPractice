import json
with open("data_file.json", "r") as read_file:
    data_base = dict(json.load(read_file))
print(len(data_base['401174755']))
