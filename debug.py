import pytesseract

try:
    tesseract_version = pytesseract.get_tesseract_version()
    print("Tesseract is installed:", tesseract_version)
except Exception as e:
    print("Tesseract Error:", e)