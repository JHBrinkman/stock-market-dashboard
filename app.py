import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import requests

# Functie om marktdata op te halen
def get_market_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")  # Laatste maand aan data
    return hist

# Functie om grote indexen op te halen
def get_index_data():
    indices = {
        "S&P 500": "^GSPC",
        "Dow Jones": "^DJI",
        "Nasdaq": "^IXIC",
        "MSCI World": "^MSCI",
        "VIX (Volatility Index)": "^VIX"
    }
    index_data = {}
    for name, symbol in indices.items():
        data = yf.Ticker(symbol).history(period="1d")
        if not data.empty:
            index_data[name] = data['Close'].iloc[-1]
    return index_data

# Streamlit UI
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📈 Live Stock Market Dashboard")

# Laat marktindexen zien
st.subheader("📊 Grote Indexen")
index_data = get_index_data()
for name, value in index_data.items():
    st.metric(label=name, value=f"${value:,.2f}")

# Gebruiker kan een ticker invoeren
ticker = st.text_input("Vul een aandelen ticker in (bijv. AAPL, TSLA, MSFT):", "AAPL").upper()

# Haal stock data op
if ticker:
    data = get_market_data(ticker)
    if not data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=ticker))
        fig.update_layout(title=f"{ticker} Aandelenkoers (Laatste Maand)", xaxis_title="Datum", yaxis_title="Prijs")
        st.plotly_chart(fig)

# Sidebar info
st.sidebar.title("ℹ️ Over deze app")
st.sidebar.info("Dit dashboard toont real-time marktinzichten, inclusief grote indexen en individuele aandelenprijzen.")

