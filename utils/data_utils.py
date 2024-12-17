# utils/data_utils.py

import json
import os

def load_data(filename):
    if os.path.exists(filename):
       with open(filename, 'r') as file:
          try:
             return json.load(file)
          except json.JSONDecodeError:
            return []
    return []

def save_data(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok = True)
    with open(filename, 'w') as file:
        json.dump(data, file, indent = 4)