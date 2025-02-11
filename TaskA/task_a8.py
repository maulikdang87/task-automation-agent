import base64
import os
import requests


def extract_credit_card():
    image_file = "./data/credit_card.png" 
    print("Checking file at:", os.path.abspath(image_file))
    output_file = "./data/credit-card.txt"
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    api_token = os.environ.get("AIPROXY_TOKEN","localhost:5432")
    print(image_file) 
    
    if not os.path.isfile(image_file):
        raise FileNotFoundError("Credit card image not found")
    if not api_token:
        raise RuntimeError("API token not found in environment variables")
    
    try:
        with open(image_file, "rb") as f:
            image_data = f.read()
        # Base64 encode the image data
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant that extracts credit card numbers from images. Output only the credit card number with no spaces."
                },
                {
                    "role": "user",
                    "content": "Here is a base64 encoded image of a credit card:\n" + encoded_image
                }
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        
        if "choices" in response_data and len(response_data["choices"]) > 0:
            card_number = response_data["choices"][0]["message"]["content"].strip().replace(" ", "")
        else:
            raise RuntimeError("Failed to extract credit card number from LLM response")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(card_number)
        
        return "Credit card number extracted successfully."
    except Exception as e:
        raise RuntimeError(f"Error extracting credit card number: {e}")
