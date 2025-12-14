import yfinance as yf

from news_providers.redis_client import r

CACHE_KEY = 'stocks_trending'
CACHE_TTL = 3600


def get_stocks_trending():

    """
    Get best performing stocks from yfinance
    """
    
    cached = r.get(CACHE_KEY)
    if cached:
        print(f'Using cached data for {CACHE_KEY}')
        return cached.decode('utf-8').split('\n\n')

    try:
        tickers = [ "AAPL", "MSFT", "GOOGL", "META", "TSLA"]
        results = []

        for ticker_symbol in tickers:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info

            current_price = info.get('currentPrice')
            previous_close = info.get('previousClose')

            if previous_close and current_price != 'N/A':
                change_percent = ((current_price - previous_close) / previous_close) * 100
                emoji = '📈' if change_percent > 0 else '📉'
            else:
                change_percent = 0
                emoji = '❌'
            
            
            company_name = info.get("longName", ticker_symbol)

        results.append(
                f"{emoji} *{company_name}* ({ticker_symbol})\n"
                f"💵 Price: ${current_price}\n"
                f"📊 Change: {change_percent:+.2f}%"
        )

        r.set(CACHE_KEY, '\n\n'.join(results), ex=CACHE_TTL)

        print(f'New data fetched for {CACHE_KEY}')
        return results
           
    except Exception as e:
        error_msg = f"Error fetching stocks: {e}"
        print(error_msg)
        return [error_msg]