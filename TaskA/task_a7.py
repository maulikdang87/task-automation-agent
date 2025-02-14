import os
import requests
from dotenv import load_dotenv

def A7():
    load_dotenv()
    
    email_file = "./data/email.txt"
    output_file = "./data/email-sender.txt"
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    api_token = os.getenv("OPENAI_API_KEY", "localhost:5432")
    
    if not os.path.isfile(email_file):
        raise FileNotFoundError("Email file not found")
    if not api_token:
        raise RuntimeError("API token not found in environment variables")
    
    try:
        with open(email_file, "r", encoding="utf-8") as f:
            email_content = f.read()
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant that extracts the sender's email address from an email message. Output only the email address."
                },
                {
                    "role": "user",
                    "content": "Here is the email message:\n\n" + email_content
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
            sender_email = response_data["choices"][0]["message"]["content"].strip()
        else:
            raise RuntimeError("Failed to extract email from LLM response")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(sender_email)
        
        return "Sender email extracted successfully."
    except Exception as e:
        raise RuntimeError(f"Error extracting sender email: {e}")
