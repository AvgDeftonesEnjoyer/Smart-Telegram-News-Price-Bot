import requests

from smart_bot.settings import COINGECKO_TRENDING_URL
from news_providers.redis_client import r

CACHE_KEY = 'crypto_trending'
CACHE_TTL = 3600 # 1 hour

def get_crypto_trending():
    
    cached = r.get(CACHE_KEY)
    if cached:
        cached_str = cached.decode('utf-8')
        print(f"Using cached data for {CACHE_KEY}")
        return cached_str.split('\n\n')
    
    try:
        response = requests.get(COINGECKO_TRENDING_URL, timeout=10)
        data = response.json()

        coins = data.get('coins', [])
        results = []

        for item in coins:
            coin = item['item']
            name = coin['name']
            symbol = coin['symbol']
            market_cap_rank = coin.get('market_cap_rank')
            price_btc = coin.get('price_btc')
            
            results.append(
                f"💰 *{name}* ({symbol.upper()})\n"
                f"🔻 Ранг: {market_cap_rank}\n"
                f"₿ Ціна в BTC: {price_btc:.8f}"
            )
        
        r.set(CACHE_KEY, '\n\n'.join(results), ex=CACHE_TTL)
        
        print(f"New data fetched for {CACHE_KEY}")
        return results
    
    except Exception as e:
        error_msg = f"Error fetching crypto trending: {e}"
        print(error_msg)
        return [error_msg]  # Return as list to match expected format
            