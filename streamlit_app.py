import streamlit as st
import yfinance as yf
import pandas_ta as ta

st.title("🚦 Swing Trader Big 5")
ticker = st.text_input("Enter Ticker:", "AAPL").upper()

if ticker:
    df = yf.download(ticker, period="max", interval="1d")
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    if len(df) > 200:
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA200'] = ta.sma(df['Close'], length=200)
        price = float(df['Close'].iloc[-1])
        
        # Get SMA200
        sma_s = df['SMA200'].dropna()
        sma200 = float(sma_s.iloc[-1]) if not sma_s.empty else 0
        
        # Get RSI
        rsi_s = df['RSI'].dropna()
        rsi_val = float(rsi_s.iloc[-1]) if not rsi_s.empty else 0
        
        st.success(f"Dashboard for {ticker}")
        col1, col2 = st.columns(2)
        col1.metric("Current Price", f"${price:,.2f}")
        col2.metric("RSI Momentum", f"{rsi_val:.1f}")
        
        st.metric("200-Day Safety Line (SMA)", f"${sma200:,.2f}")
        
        if price > sma200:
            st.write("🟢 Price is ABOVE the 200-day line (Healthy Trend)")
        else:
            st.write("🔴 Price is BELOW the 200-day line (Use Caution)")
    else:
        st.error("Not enough historical data for this ticker.")
        # Volume Math
        curr_vol = float(df['Volume'].iloc[-1])
        avg_vol = float(df['Volume'].rolling(window=20).mean().iloc[-1])
        vol_ratio = (curr_vol / avg_vol)
        
        # Add this to your display section (e.g., in a new column or below)
        st.divider()
        st.subheader("Volume Analysis")
        if curr_vol > avg_vol:
            st.write(f"🟢 High Volume: {vol_ratio:.2f}x the 20-day average.")
        else:
            st.write(f"⚪ Low Volume: {vol_ratio:.2f}x the 20-day average.")        
