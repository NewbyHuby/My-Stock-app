import streamlit as st
import yfinance as yf
import pandas_ta as ta

st.title("🚦 Swing Trader Big 5")
ticker = st.text_input("Enter Ticker:", "AAPL").upper()

if ticker:
    df = yf.download(ticker, period="2y", interval="1d")
    if not df.empty and len(df) > 200:
        df['EMA9'] = ta.ema(df['Close'], length=9)
        df['EMA21'] = ta.ema(df['Close'], length=21)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA200'] = ta.sma(df['Close'], length=200)
        df = df.dropna()
        if not df.empty:
            price = float(df['Close'].iloc[-1])
            rsi_val = float(df['RSI'].iloc[-1])
            st.subheader(f"{ticker}: ${price:,.2f}")
            st.write(f"RSI: {rsi_val:.1f}")
        else:
            st.error("Calculations failed. Try a different ticker.")
