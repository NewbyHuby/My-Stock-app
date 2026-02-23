import streamlit as st
import yfinance as yf
import pandas_ta as ta

st.set_page_config(page_title="Swing Signal", layout="centered")
st.title("🚦 Swing Trader Big 5")

ticker = st.text_input("Enter Ticker (e.g., AAPL, TSLA):", "AAPL").upper()

if ticker:
    df = yf.download(ticker, period="1y", interval="1d")
    if not df.empty:
        df['EMA9'] = ta.ema(df['Close'], length=9)
        df['EMA21'] = ta.ema(df['Close'], length=21)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA200'] = ta.sma(df['Close'], length=200)
        macd = ta.macd(df['Close'])
        
        price = float(df['Close'].iloc[-1])
        rsi_val = float(df['RSI'].iloc[-1])
        ema9 = float(df['EMA9'].iloc[-1])
        ema21 = float(df['EMA21'].iloc[-1])
        sma200 = float(df['SMA200'].iloc[-1])
        
        vol_curr = float(df['Volume'].iloc[-1])
        vol_avg = float(df['Volume'].rolling(20).mean().iloc[-1])

        def get_light(condition):
            return "🟢" if condition else "🔴"

        st.subheader(f"Status for {ticker}: ${price:,.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Trend (EMA 9/21)", f"{get_light(ema9 > ema21)}")
            st.write(f"9: {ema9:,.2f} | 21: {ema21:,.2f}")
            st.metric("RSI (Momentum)", f"{rsi_val:.1f}")
            st.caption("Target: 40-60 for Swing")

        with col2:
            st.metric("Institutional Vol", f"{get_light(vol_curr > vol_avg)}")
            st.write(f"Vol is {((vol_curr/vol_avg)*100):.0f}% of avg")
            st.metric("Safety (SMA 200)", f"{get_light(price > sma200)}")
            st.write(f"200 Day: {sma200:,.2f}")

        st.divider()
        if not macd.empty:
            macd_hist = float(macd.iloc[-1, 1])
            st.write("MACD Trend Strength: " + ("Rising 📈" if macd_hist > 0 else "Fading 📉"))
    else:
        st.error("Ticker not found.")
