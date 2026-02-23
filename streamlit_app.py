import streamlit as st
import yfinance as yf
import pandas_ta as ta

st.title("🚦 Swing Trader Big 5")
ticker = st.text_input("Enter Ticker:", "AAPL").upper()

if ticker:
    df = yf.download(ticker, period="2y", interval="1d")
    if len(df) > 200:
        # Calculations
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA200'] = ta.sma(df['Close'], length=200)
        
        # Grab the very last valid numbers
        last_row = df.iloc[-1]
        price = float(last_row['Close'])
        # If RSI is empty for today, look back one day
        \rsi_val = df['RSI'].dropna().iloc[-1]
        
        st.success(f"Connected to {ticker}!")
        st.subheader(f"Current Price: ${price:,.2f}")
        st.write(f"RSI Momentum: {rsi_val:.1f}")
    else:
        st.error("Please enter a valid stock ticker with at least 1 year of history.")
