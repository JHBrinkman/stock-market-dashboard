import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Beschikbare indices (MSCI World vervangen door URTH)
indices = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "Nasdaq": "^IXIC",
    "MSCI World (via URTH ETF)": "URTH",
    "VIX (Volatility Index)": "^VIX"
}

# Periode opties voor historische data
period_options = {
    "1 dag": "1d",
    "7 dagen": "7d",
    "4 weken": "1mo",
    "6 maanden": "6mo",
    "12 maanden": "12mo"
}

# Functie om marktdata op te halen
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

st.title("📊 Grote Aandelenmarkten Dashboard")

# Keuzemenu voor index
selected_index_label = st.selectbox("Selecteer een marktindex:", list(indices.keys()))
selected_index = indices[selected_index_label]

# Keuzemenu voor tijdsperiode
selected_period_label = st.selectbox("Selecteer een periode:", list(period_options.keys()))
selected_period = period_options[selected_period_label]

# Haal index data op
data = get_market_data(selected_index, selected_period)
if not data.empty:
    percentage_change = calculate_percentage_change(data)
    
    # Grafiek maken
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=selected_index_label))
    
    # Titel aanpassen met procentuele verandering
    change_text = f"({percentage_change:+.2f}%)" if percentage_change is not None else ""
    fig.update_layout(
        title=f"{selected_index_label} Koers over {selected_period_label} {change_text}",
        xaxis_title="Datum",
        yaxis_title="Prijs",
        template="plotly_white"
    )
    
    # Grafiek weergeven
    st.plotly_chart(fig)

    # Extra metric weergeven
    st.metric(label=f"Procentuele verandering ({selected_period_label})", value=f"{percentage_change:+.2f}%" if percentage_change is not None else "Geen data")
else:
    st.error("Geen data beschikbaar voor deze periode.")
