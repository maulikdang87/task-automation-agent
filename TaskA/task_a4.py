import json
import os

def A4():
    """
    Sorts the array of contacts in /data/contacts.json by last_name, then first_name,
    and writes the result to /data/contacts-sorted.json.
    """
    # Define the local data directory.
    local_data_dir = os.path.join(os.getcwd(), "data")
    
    # Construct paths for the input and output files.
    contacts_path = os.path.join(local_data_dir, "contacts.json")
    sorted_contacts_path = os.path.join(local_data_dir, "contacts-sorted.json")
    
    # Ensure contacts.json exists.
    if not os.path.exists(contacts_path):
        raise Exception(f"File not found: {contacts_path}")
    
    # Read contacts.json.
    with open(contacts_path, "r") as f:
        try:
            contacts = json.load(f)
        except Exception as e:
            raise Exception("Error reading contacts.json: " + str(e))
    
    # Sort contacts by last_name and then first_name.
    sorted_contacts = sorted(
        contacts,
        key=lambda c: (c.get("last_name", "").lower(), c.get("first_name", "").lower())
    )
    
    # Write the sorted contacts to contacts-sorted.json with indentation.
    with open(sorted_contacts_path, "w") as f:
        json.dump(sorted_contacts, f, indent=2)
    
    return {"sorted_contacts": sorted_contacts}