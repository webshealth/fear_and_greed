import os
import requests
import json
from datetime import datetime, timezone

def main():
    api_key = os.getenv("APITUBE_API_KEY")
    if not api_key:
        print(json.dumps({
            "status": "error",
            "message": "API key not found",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))
        return

    url = f"https://api.apitube.io/v1/news/everything?api_key={api_key}&per_page=1"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        result = {
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {
                "articles_count": len(data.get("articles", [])),
                "first_article_title": data.get("articles", [{}])[0].get("title", "N/A")
            }
        }
        print(json.dumps(result, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(json.dumps({
            "status": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": type(e).__name__,
            "message": str(e)
        }, ensure_ascii=False))

if __name__ == "__main__":
    main()
