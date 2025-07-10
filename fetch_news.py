import os
import requests
import json
from datetime import datetime

def main():
    api_key = os.getenv("APITUBE_API_KEY")
    if not api_key:
        print("API key not found!")
        return

    url = f"https://api.apitube.io/v1/news/everything?api_key={api_key}&per_page=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Create structured output
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success",
            "data": data
        }
        
        # Print JSON to stdout (will be captured in output.json)
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "error",
            "message": str(e)
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
