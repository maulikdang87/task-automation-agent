# B3: Fetch Data from an API

import requests
from TaskB.task_b12 import B12

def B3(url, save_path):
    if not B12(save_path):
        return None
    
    save_path = save_path.lstrip('/')
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)