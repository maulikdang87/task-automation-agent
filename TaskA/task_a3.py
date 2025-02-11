import os
from datetime import datetime

def parse_date(date_str):
    date_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%b %d, %Y",
        "%d-%b-%Y",
        "%Y/%m/%d",
        "%d-%b-%Y %H:%M:%S",
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def count_wednesdays():
    input_file = "./data/dates.txt"
    output_file = "./data/dates-wednesdays.txt"
    
    if not os.path.isfile(input_file):
        raise FileNotFoundError("dates.txt not found")
    
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            dates = file.readlines()
        
        wednesday_count = sum(1 for date in dates if parse_date(date.strip()) and parse_date(date.strip()).weekday() == 2)
        
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(str(wednesday_count))
        
        return "Wednesday count written successfully."
    except Exception as e:
        raise RuntimeError(f"Error processing dates: {e}")
