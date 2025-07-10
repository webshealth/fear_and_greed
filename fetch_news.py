import os
import requests
import json

def main():
    # Get API key from environment variables
    api_key = os.getenv("APITUBE_API_KEY")
    if not api_key:
        print("API key not found in environment variables!")
        return

    # Make API request
    url = f"https://api.apitube.io/v1/news/everything?api_key={api_key}&per_page=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        print("API Response:")
        print(json.dumps(data, indent=2))
        
        # Add your processing logic here
        # Example: extract_title = data['articles'][0]['title']
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError:
        print("Failed to parse JSON response")

if __name__ == "__main__":
    main()
