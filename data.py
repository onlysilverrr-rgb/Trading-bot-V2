
import requests

from config import API_KEY, CANDLES


BASE_URL = "https://api.twelvedata.com/time_series"


def get_market_data(symbol, interval):

    params = {

        "symbol": symbol,
        "interval": interval,
        "outputsize": CANDLES,
        "apikey": API_KEY

    }

    try:

        response = requests.get(BASE_URL, params=params, timeout=20)

        data = response.json()

        if "values" not in data:

            print(data.get("message", "No data returned"))
            return None

        print(f"✅ {symbol} | {interval} | {len(data['values'])} candles")

        return data

    except Exception as e:

        print(f"❌ Error downloading {symbol}")
        print(e)

        return None

