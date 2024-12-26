import requests
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_historical_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "gbp", "days": "7", "interval": "daily"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        prices = data.get("prices", [])
        timestamps = [datetime.utcfromtimestamp(price[0] / 1000) for price in prices]
        values = [price[1] for price in prices]
        return timestamps, values
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return [], []

def plot_historical_chart(coin_id, coin_name):
    timestamps, values = fetch_historical_data(coin_id)
    if timestamps and values:
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, values, marker="o", linestyle="-", label=coin_name)
        plt.title(f"{coin_name} Historical Price (7 Days)")
        plt.xlabel("Date")
        plt.ylabel("Price (GBP)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print(f"Failed to plot data for {coin_name}.")

# Call this function for each cryptocurrency
if __name__ == "__main__":
    plot_historical_chart("ethereum", "Ethereum")
    plot_historical_chart("litecoin", "Litecoin")
    plot_historical_chart("the-sandbox", "Sandbox")
    plot_historical_chart("chiliz", "Chiliz")
    plot_historical_chart("floki", "Floki")
