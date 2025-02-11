import json
import os
def sort_contacts():
    input_file = "./data/contacts.json"
    output_file = "./data/contacts-sorted.json"
    
    if not os.path.isfile(input_file):
        raise FileNotFoundError("contacts.json not found")
    
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            contacts = json.load(file)
        
        sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
        
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(sorted_contacts, file, indent=4)
        
        return "Contacts sorted successfully."
    except Exception as e:
        raise RuntimeError(f"Error sorting contacts: {e}")
