from datetime import datetime
import os

def A3():
    """
    Reads data/dates.txt, counts the number of Wednesdays,
    and writes the count to data/dates-wednesdays.txt.
    """
    # Define the local data directory and file paths.
    local_data_dir = os.path.join(os.getcwd(), "data")
    input_file = os.path.join(local_data_dir, "dates.txt")
    output_file = os.path.join(local_data_dir, "dates-wednesdays.txt")

    if not os.path.exists(input_file):
        raise Exception(f"File not found: {input_file}")

    # Define a list of possible date formats.
    date_formats = [
        "%Y/%m/%d %H:%M:%S",  # e.g., 2008/04/22 06:26:02
        "%Y-%m-%d",           # e.g., 2006-07-21
        "%b %d, %Y",          # e.g., Sep 11, 2006
        "%d-%b-%Y",           # e.g., 28-Nov-2021
    ]

    wednesday_count = 0

    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            parsed_date = None
            # Try each date format until one succeeds.
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(line, fmt)
                    break  # Exit loop if parsing is successful.
                except ValueError:
                    continue

            if parsed_date is None:
                # Optionally log the unparsable line.
                print(f"Warning: Could not parse date: {line}")
                continue

            # datetime.weekday() returns Monday=0, Tuesday=1, Wednesday=2, etc.
            if parsed_date.weekday() == 2:
                wednesday_count += 1


    # Write just the count to the output file.
    with open(output_file, "w") as file:
        file.write(str(wednesday_count))

    return {"wednesday_count": wednesday_count}