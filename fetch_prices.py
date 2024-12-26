import yfinance as yf  # Import yfinance to fetch stock data
import requests  # Import requests to fetch cryptocurrency data from CoinGecko

"""
Fetch Prices Script

Current Features:
1. Cryptocurrency Data:
   - Pulls live prices, 24-hour changes, and 7-day changes for Bitcoin, Ethereum, and Litecoin from the CoinGecko API.
   - Handles both USD and GBP currencies and formats the data neatly for use.
   - Logs any errors to the console if something goes wrong (e.g., API timeout).

2. Stock Data:
   - Uses Yahoo Finance (via `yfinance`) to get the latest closing prices for stocks like S&P 500, Tesla, Nio, and Apple.
   - Ensures the program doesn’t crash if the stock data is unavailable or incomplete.

3. Combined Data:
   - Merges crypto and stock data into one dictionary so the dashboard can display everything seamlessly.
   - Keeps going even if one source (crypto or stocks) fails, ensuring the program remains functional.

Future Improvements:
1. Add More Cryptos:
   - Expand the list of tracked cryptocurrencies dynamically—maybe let users pick what they want to monitor.

2. Include More Stock Info:
   - Add interesting details like daily highs, lows, market caps, or trading volume for a more complete picture.

3. Multi-Currency Support:
   - Let users view prices in their preferred currency (e.g., EUR, JPY) for better global usability.

4. Real-Time Stock Updates:
   - Move beyond daily closing prices and include real-time intraday updates for stocks.

5. Smarter Error Handling:
   - Retry API requests automatically if something fails, and back off gracefully to avoid rate limits.

6. Logging:
   - Save fetched data and errors to a file so you can track trends or debug issues later.

7. API Optimization:
   - Reduce unnecessary API calls by caching data and refreshing only when needed.

8. User Customization:
   - Add a configuration file so users can easily set up their preferences like tracked assets, currencies, or thresholds.

"""

import yfinance as yf  # Import yfinance to fetch stock data
import requests  # Import requests to fetch cryptocurrency data from CoinGecko

def fetch_crypto_prices():
    """
    Fetch the current prices and 24-hour changes for cryptocurrencies from the CoinGecko API.
    :return: Dictionary containing price and percentage change data for each cryptocurrency.
    """
    # Define the cryptocurrencies to fetch with their CoinGecko IDs
    coins = {
        "bitcoin": "Bitcoin",  # Bitcoin (BTC)
        "ethereum": "Ethereum",  # Ethereum (ETH)
        "litecoin": "Litecoin",  # Litecoin (LTC)
        "ripple": "XRP",  # Ripple (XRP)
        "monero": "Monero",  # Monero (XMR)
        "cardano": "Cardano",  # Cardano (ADA)
        "dogecoin": "Dogecoin"  # Dogecoin (DOGE)
    }

    # API endpoint and parameters for CoinGecko's simple price API
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coins.keys()),  # Join cryptocurrency IDs into a comma-separated string
        "vs_currencies": "usd,gbp",  # Fetch prices in USD and GBP
        "include_24hr_change": "true",  # Include 24-hour percentage changes
        "include_7d_change": "true"  # Include 7-day percentage changes
    }

    try:
        # Send a GET request to the CoinGecko API
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an error if the response status is not 200
        data = response.json()  # Parse the JSON response

        # Initialize an empty dictionary to store results
        results = {}
        # Loop through each cryptocurrency and extract its data
        for coin_id, coin_name in coins.items():
            price_gbp = data.get(coin_id, {}).get("gbp", "N/A")  # Get the price in GBP
            change_24hr = data.get(coin_id, {}).get("gbp_24h_change", "N/A")  # Get the 24-hour change
            change_7d = data.get(coin_id, {}).get("gbp_7d_change", "N/A")  # Get the 7-day change

            # Format the price and percentage changes if valid, otherwise set as "N/A"
            price_gbp = f"{price_gbp:.2f}" if isinstance(price_gbp, (float, int)) else "N/A"
            change_24hr = f"{change_24hr:.2f}%" if isinstance(change_24hr, (float, int)) else "N/A"
            change_7d = f"{change_7d:.2f}%" if isinstance(change_7d, (float, int)) else "N/A"

            # Add the formatted data to the results dictionary
            results[coin_name] = {
                "price": price_gbp,
                "change_24hr": change_24hr,
                "change_7d": change_7d
            }

        return results  # Return the dictionary of results

    except Exception as e:
        # Print an error message if the API request fails
        print(f"Error fetching cryptocurrency data: {e}")
        return None  # Return None if an error occurs

def fetch_stock_prices():
    """
    Fetch the current prices for stocks using the yfinance library.
    :return: Dictionary containing the latest prices for each stock.
    """
    # Define the stocks to fetch with their Yahoo Finance tickers
    stocks = {
        "S&P 500": "^GSPC",  # S&P 500 index
        "Tesla": "TSLA",  # Tesla Inc.
        "Nio": "NIO",  # Nio Inc.
        "Apple": "AAPL"  # Apple Inc.
    }

    # Initialize an empty dictionary to store results
    results = {}
    try:
        # Loop through each stock and fetch its data
        for stock_name, ticker in stocks.items():
            stock = yf.Ticker(ticker)  # Create a yfinance Ticker object
            stock_data = stock.history(period="1d")  # Fetch the latest day's data
            if not stock_data.empty:  # Check if the data is not empty
                current_price = stock_data["Close"].iloc[-1]  # Get the latest closing price
                # Add the price to the results dictionary
                results[stock_name] = {
                    "price": f"{current_price:.2f}"
                }
            else:
                # If no data is available, set the price as "N/A"
                results[stock_name] = {"price": "N/A"}

        return results  # Return the dictionary of results

    except Exception as e:
        # Print an error message if fetching stock data fails
        print(f"Error fetching stock data: {e}")
        return None  # Return None if an error occurs

def fetch_prices():
    """
    Fetch prices for both cryptocurrencies and stocks by combining the results of 
    fetch_crypto_prices and fetch_stock_prices.
    :return: A combined dictionary of all assets and their respective data.
    """
    # Fetch cryptocurrency data
    crypto_data = fetch_crypto_prices() or {}  # Default to an empty dictionary if None
    # Fetch stock data
    stock_data = fetch_stock_prices() or {}  # Default to an empty dictionary if None

    # Combine cryptocurrency and stock data into a single dictionary
    return {**crypto_data, **stock_data}
