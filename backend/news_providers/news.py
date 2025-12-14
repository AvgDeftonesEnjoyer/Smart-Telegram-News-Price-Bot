import requests

from django.conf import settings
from news_providers.redis_client import r

CACHE_KEY = 'new_trending'
CACHE_TTL = 1800

def get_news_trending(category: str = 'business'):
    """
    Get trending news from newsapi
    """
    
    cached = r.get(CACHE_KEY)
    if cached:
        print(f'Using cached data for {CACHE_KEY}')
        return cached.decode('utf-8').split('\n\n')
    
    try:
        api_key = settings.NEW_API_KEY
        url = 'https://newsapi.org/v2/top-headlines'

        params = {
            'apiKey': api_key,
            'country': "us",
            'category': category,
            'pageSize': 5
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        articles = data.get('articles', [])

        if not articles:
            return ["No news available at the moment."]

        results = []
        for article in articles:
            title = article.get('title', 'No title')
            source = article.get('source', {}).get('name', 'Unknown')
            url = article.get('url', '')
            description = article.get('description', '')
            
            if description and len(description) > 150:
                description = description[:147] + '...'
            
            results.append(
                f"📰 *{title}*\n"
                f"🏢 Source: {source}\n"
                f"📝 {description}\n"
                f"🔗 {url}"
            )
        

        r.set(CACHE_KEY, '\n\n'.join(results), ex=CACHE_TTL)
        
        print(f"New data fetched for {CACHE_KEY}")
        return results
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error fetching news: {e}"
        print(error_msg)
        return [error_msg]
        
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        return [error_msg]