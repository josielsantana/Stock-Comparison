import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from yahooquery import Ticker
import time

st.set_page_config(page_title="Stock Comparison", layout="centered")
st.title("📈 Brazilian Stock Comparison - B3")

col1, col2 = st.columns(2)
with col1:
    input1 = st.text_input("Ticker1", value="PETR4")
with col2:
    input2 = st.text_input("Ticker2", value="VALE3")


if st.button("🔍 Analyze"):
    try:
        today = time.strftime("%Y-%m-%d")
        df1 = Ticker(f"{input1}.SA").history(start=f"{time.strftime('%Y')}-01-01", end=today)
        df2 = Ticker(f"{input2}.SA").history(start=f"{time.strftime('%Y')}-01-01", end=today)

        df1["ROI"] = df1["close"] / df1["close"].iloc[0] - 1
        df2["ROI"] = df2["close"] / df2["close"].iloc[0] - 1

        df1 = df1.reset_index()[["date", "ROI", "symbol"]]
        df2 = df2.reset_index()[["date", "ROI", "symbol"]]
        df = pd.concat([df1, df2])

        sns.set_style("whitegrid")
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x="date", y="ROI", hue="symbol")
        plt.title("YTD ROI Comparsion")
        plt.ylabel("Return (%)")
        plt.xlabel("Date")
        plt.tight_layout()

        st.pyplot(plt.gcf())

    except Exception as e:
        st.error(f"Erro ao buscar os dados: {e}")
