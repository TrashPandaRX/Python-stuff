import json
import os

# WORKS!
_path = os.path.dirname(__file__) + "/json_files/Hero_with Resist.json"

with open(_path) as file:
    data = json.load (file)

print(data)