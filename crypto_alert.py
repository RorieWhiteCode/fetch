import requests
import winsound  # For sound alerts on Windows
import time

def play_alert(coin_name, change):
    frequency = 1000  # Set Frequency in Hz
    duration = 500  # Set Duration in ms
    print(f"ALERT: {coin_name} has changed by {change}%!")
    for _ in range(3):  # Play sound 3 times
        winsound.Beep(frequency, duration)

def fetch_and_check_alerts():
    coins = {
        "ethereum": "Ethereum",
        "litecoin": "Litecoin",
        "the-sandbox": "Sandbox",
        "chiliz": "Chiliz",
        "floki": "Floki"
    }
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coins.keys()),
        "vs_currencies": "gbp",
        "include_24hr_change": "true"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        for coin_id, coin_name in coins.items():
            change_24hr = data.get(coin_id, {}).get("gbp_24h_change", 0)

            if isinstance(change_24hr, (float, int)) and abs(change_24hr) >= 10:
                play_alert(coin_name, change_24hr)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_check_alerts()
        time.sleep(300)  # Check every 5 minutes
