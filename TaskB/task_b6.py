
import requests

def B6(url, output_filename):
    
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result