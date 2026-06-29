
import mplfinance as mpf
import pandas as pd


def save_chart(df, market):

    chart = df.copy()

    chart = chart.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    })

    chart.index = pd.to_datetime(df["datetime"])

    apds = [
        mpf.make_addplot(chart["EMA20"]),
        mpf.make_addplot(chart["EMA50"])
    ]

    filename = f"{market.replace('/','_')}.png"

    mpf.plot(
        chart,
        type="candle",
        style="yahoo",
        mav=(20,50),
        volume=True,
        addplot=apds,
        savefig=filename
    )

    return filename

