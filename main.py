import os
import requests
import json
import sys
from datetime import datetime, timezone

def main():
    # Get API key from environment variables
    api_key = os.getenv("APITUBE_API_KEY")
    if not api_key:
        result = {
            "status": "error",
            "message": "API key not found in environment variables",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        print(json.dumps(result))
        return

    # Construct API URL
    url = f"https://api.apitube.io/v1/news/everything?api_key={api_key}&per_page=1"
    
    try:
        # Make API request
        response = requests.get(url, timeout=10)  # 10-second timeout
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Process response
        data = response.json()
        result = {
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {
                "articles_count": len(data.get("articles", [])),
                "first_article_title": data.get("articles", [{}])[0].get("title", "N/A")
            }
        }
        
        # Print result to stdout (captured in output.json)
        print(json.dumps(result, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        error_result = {
            "status": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": type(e).__name__,
            "message": str(e)
        }
        print(json.dumps(error_result, ensure_ascii=False))
    except Exception as e:
        error_result = {
            "status": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": "UnexpectedError",
            "message": f"Unexpected error: {str(e)}"
        }
        print(json.dumps(error_result, ensure_ascii=False))

if __name__ == "__main__":
    main()
