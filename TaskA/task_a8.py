from PIL import Image , ImageEnhance
import os
import pytesseract
import re

def A8():
    """
    1. Reads /mnt/data/credit_card.png
    2. Extracts a clean 16-digit number via Tesseract OCR
    3. Applies Luhn check. If it fails and the first digit is '9',
       try replacing it with '3' and check again.
    4. Writes the final 16-digit number to /mnt/data/credit-card.txt
    """
    input_file = os.path.join(os.getcwd(), "data", "credit_card.png")
    output_file = os.path.join(os.getcwd(), "data", "credit-card.txt")

    # Set Tesseract path
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    try:
        # 1. Load the image
        img = Image.open(input_file)
        img = Image.open(input_file).convert("L")  # Convert to grayscale
        img = ImageEnhance.Contrast(img).enhance(2)  # Increase contrast
        img = ImageEnhance.Sharpness(img).enhance(2)

        # 2. Configure Tesseract for digits only
        custom_config = r"--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789"
        extracted_text = pytesseract.image_to_string(img, config=custom_config)

        # 3. Extract the first standalone 16-digit number using regex
        match = re.search(r"\b\d{16}\b", extracted_text)  
        if not match:
            return {"error": "OCR failed to extract exactly 16 digits.", "ocr_output": extracted_text}

        recognized_16 = match.group()
        
        misread_fixes = {"O": "0", "l": "1", "B": "8", "S": "5"}
        for char, correct in misread_fixes.items():
            recognized_16 = recognized_16.replace(char, correct)

        # 4. Check Luhn validity
        if passes_luhn(recognized_16):
            final_number = recognized_16
        else:
            # If first digit is '9', try replacing it with '3'
            if recognized_16[0] == '9':
                possible_fix = '3' + recognized_16[1:]
                if passes_luhn(possible_fix):
                    final_number = possible_fix
                else:
                    return {"error": "Luhn check failed, flipping '9'->'3' also failed.", "recognized_number": recognized_16}
            else:
                return {"error": "Luhn check failed and no known fix.", "recognized_number": recognized_16}

        # 5. Write final_number to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_number + "\n")

        return {"written_file": output_file, "card_number": final_number}

    except Exception as e:
        return {"error": str(e)}

def passes_luhn(number_str: str) -> bool:
    """Returns True if 'number_str' (containing only digits) satisfies the Luhn check."""
    if not number_str.isdigit():
        return False
    
    digits = [int(d) for d in number_str]
    # Double every second digit from the right
    for i in range(len(digits) - 2, -1, -2):
        doubled = digits[i] * 2
        if doubled > 9:
            doubled -= 9
        digits[i] = doubled
    
    return sum(digits) % 10 == 0
