import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("S&P 500 App")

st.markdown("""
This app retrieves the list of the ***S&P 500*** (from Wikipedia) and its corresponding
closing price (year-to-date)

* **Python Libraries:** base64, pandas, streamlit, matplotlib, yfinance
            
* **Data Source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
""")

st.sidebar.header("User Input Features")

# Web Scraping of S&P 500 data
@st.cache_data
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

# Download S&P 500 data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

# Plot closing Price of Query Symbol
def price_plot(symbol):

    if symbol in data:
        df2 = pd.DataFrame(data[symbol]["Close"]).reset_index()
        plt.fill_between(df2["Date"], df2["Close"], color="skyblue", alpha=0.3)
        plt.plot(df2["Date"], df2["Close"], color="skyblue", alpha=0.8)
        plt.xticks(rotation=45)
        plt.xlabel("Date", fontweight="bold")
        plt.ylabel("Close Price", fontweight="bold")
        plt.title(f"{symbol} ({df[df['Symbol'] == symbol]['Security'].values[0]})", fontweight='bold')

    else:
        st.warning(f"Data for symbol {symbol} not found.")
    return st.pyplot()


df = load_data()

# Sidebar -Sector selection
sector = df.groupby("GICS Sector")
sorted_sector_unique = sorted(df["GICS Sector"].unique())
selected_sector = st.sidebar.multiselect("Sector", sorted_sector_unique)

# Filtering Data
df_selected_sector = df[(df["GICS Sector"]).isin(selected_sector)]
tickers_in_selected_sector = sorted(list(df_selected_sector["Symbol"]))
# num_company = st.sidebar.slider("Number of Companies to Plot", 1, 10)

custom_ticker = st.sidebar.toggle('Choose Specific Ticker(s)')

if custom_ticker:
    chosen_ticker = st.sidebar.multiselect(f"Tickers to Plot (Max. 5)", tickers_in_selected_sector, max_selections=5)


st.header("Display Companies in Selected Sector")
st.write("Data Dimensions: " + str(df_selected_sector.shape[0]) + " rows and " + str (df_selected_sector.shape[1]) + " columns" )

st.dataframe(df_selected_sector, hide_index=True)

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)


# Get financial data
if len(selected_sector) > 0:
    data = yf.download(
            tickers = sorted(list(df_selected_sector["Symbol"])),
            period = "ytd",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            prepost=True,
            threads=True,
            proxy=None
    )

if st.button("Show Plots"):
    st.header("Stock Closing Price")

    if custom_ticker:

        for i in chosen_ticker:
            price_plot(i)
        

    else:

        for j in df_selected_sector["Symbol"][:5]:
            price_plot(j)

