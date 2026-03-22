import streamlit as st
import requests
import time
from datetime import datetime
import yfinance as yf

# --- Hacker Theme CSS ---
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: #00FF41;
    font-family: 'Courier New', Courier, monospace;
}
/* Make the stock price numbers white */
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Kevin's Dashboard")
st.write(f"**Days that have passed this year:** {datetime.now().timetuple().tm_yday}")

# --- Weather Section ---
API_KEY = "823fb41589e0322d1cb0df6b2db7df68"
url = f"http://api.openweathermap.org/data/2.5/weather?q=Davie,FL,US&appid={API_KEY}&units=imperial"

try:
    res = requests.get(url).json()
    if str(res.get("cod")) != "200":
        st.error(f"API Error: {res.get('message')}")
    else:
        weather = res['weather'][0]['description'].title()
        temp = res['main']['temp']
        st.write(f"**Current Weather:** {weather}, {temp}°F")
        
        now = time.time()
        sunset, sunrise = res['sys']['sunset'], res['sys']['sunrise']
        
        if sunrise < now < sunset:
            diff = sunset - now
            event = "Sunset"
        else:
            diff = (sunrise + 86400 - now) if now > sunset else (sunrise - now)
            event = "Sunrise"

        hours, remainder = divmod(diff, 3600)
        st.write(f"**Time until {event}:** {int(hours)}h {int(remainder // 60)}m")
        
except Exception as e:
    st.write(f"Error: {e}")

st.write("---")

# --- Stocks Section ---
st.subheader("My Stocks")
tickers = ['FLO', 'SCHD', 'CSX', 'PFE', 'REYN', 'CAG', 'ULTY' , 'HFXI']
selected = st.multiselect("Choose stocks:", tickers, default=tickers)

timeframes = {"1 Week": "5d", "1 Month": "1mo", "6 Months": "6mo", "1 Year": "1y"}
selected_time = st.selectbox("Timeframe:", list(timeframes.keys()))

if selected:
    data = yf.download(selected, period=timeframes[selected_time])['Close']
    
    for i in range(0, len(selected), 3):
        cols = st.columns(3)
        for j, ticker in enumerate(selected[i:i+3]):
            current = data[ticker].iloc[-1] if len(selected) > 1 else data.iloc[-1]
            start = data[ticker].iloc[0] if len(selected) > 1 else data.iloc[0]
            
            cols[j].metric(ticker, f"${float(current):.2f}", f"{float(current - start):.2f}")
            
    # Chart with the Matrix/Hacker green color
    st.line_chart(data, color=["#00FF41"] * len(selected))

st.write("---")

# --- Notes Section ---
with st.expander("ℹ️ Info & Notes"):
    st.write("program information")
    st.write("the python file name is kevin dashboard.py")
    st.write("weather and stock information on my dashboard")
