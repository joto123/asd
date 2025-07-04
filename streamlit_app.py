# streamlit_app.py
import streamlit as st
import ccxt
import time

binance = ccxt.binance()
kraken = ccxt.kraken()
symbol = 'BTC/USDT'
threshold = 0.3

st.set_page_config(page_title="Крипто Арбитраж AI", layout="centered")
st.title("🤖 AI Наблюдател за Арбитраж")
placeholder = st.empty()

def get_prices():
    b_bid, b_ask = binance.fetch_order_book(symbol)['bids'][0][0], binance.fetch_order_book(symbol)['asks'][0][0]
    k_bid, k_ask = kraken.fetch_order_book(symbol)['bids'][0][0], kraken.fetch_order_book(symbol)['asks'][0][0]
    return b_bid, b_ask, k_bid, k_ask

while True:
    b_bid, b_ask, k_bid, k_ask = get_prices()

    recs = []
    spread_1 = ((k_bid - b_ask) / b_ask) * 100
    spread_2 = ((b_bid - k_ask) / k_ask) * 100

    if spread_1 > threshold:
        recs.append(f"💡 Купи в Binance ({b_ask:.2f}), продай в Kraken ({k_bid:.2f}) → +{spread_1:.2f}%")
    if spread_2 > threshold:
        recs.append(f"💡 Купи в Kraken ({k_ask:.2f}), продай в Binance ({b_bid:.2f}) → +{spread_2:.2f}%")
    if not recs:
        recs.append("Няма арбитражни възможности в момента.")

    with placeholder.container():
        st.metric("Binance Ask", f"${b_ask:.2f}")
        st.metric("Kraken Bid", f"${k_bid:.2f}")
        st.write("---")
        for r in recs:
            st.success(r)

    time.sleep(60)
