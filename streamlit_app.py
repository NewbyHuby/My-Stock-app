import streamlit as st
import yfinance as yf
import pandas_ta as ta

st.set_page_config(page_title="Swing Signal", layout="centered")
st.title("🚦 Swing Trader Big 5")

ticker = st.text_input("Enter Ticker (e.g., AAPL, TSLA):", "AAPL").upper()

if ticker:
df = yf.download(ticker, period="1y", interval="1d")
