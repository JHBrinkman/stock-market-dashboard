import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Functie om marktdata op te halen voor verschillende periodes
def get_market_data(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

# Functie om procentuele verandering te berekenen
def calculate_percentage_change(data):
    if not data.empty:
        start_price = data['Close'].iloc[0]
        end_price = data['Close'].iloc[-1]
        percentage_change = ((end_price - start_price) / start_price) * 100
        return percentage_change
    return None

# Streamlit UI
st.set_page_config(page_title="📈 Stock Market Dashboard", layout="wide")

st.title("📊 Live Stock Market Dashboard")

# Gebruiker kan een ticker invoeren
ticker = st.text_input("Vul een aandelen ticker in (bijv. AAPL, TSLA, MSFT):", "AAPL").upper()

# Keuzemenu voor tijdsperiode
period_options = {
    "1 dag": "1d",
    "7 dagen": "7d",
    "4 weken": "1mo",
    "6 maanden": "6mo",
    "12 maanden": "12mo"
}
selected_period_label = st.selectbox("Selecteer een periode:", list(period_options.keys()))
selected_period = period_options[selected_period_label]

# Haal stock data op
if ticker:
    data = get_market_data(ticker, selected_period)
    if not data.empty:
        percentage_change = calculate_percentage_change(data)
        
        # Grafiek maken
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=ticker))
        
        # Titel aanpassen met procentuele verandering
        change_text = f"({percentage_change:+.2f}%)" if percentage_change is not None else ""
        fig.update_layout(
            title=f"{ticker} Aandelenkoers over {selected_period_label} {change_text}",
            xaxis_title="Datum",
            yaxis_title="Prijs",
            template="plotly_white"
        )
        
        # Grafiek weergeven
        st.plotly_chart(fig)

        # Extra percentage weergeven als metric
        st.metric(label=f"Procentuele verandering ({selected_period_label})", value=f"{percentage_change:+.2f}%" if percentage_change is not None else "Geen data")
    else:
        st.error("Geen data beschikbaar voor deze periode.")
