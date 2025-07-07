import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from yahooquery import Ticker
import time
import numpy as np


st.set_page_config(page_title="Stock Comparison", layout="centered")
st.title("📈 Brazilian Stock Comparison - B3")

col1, col2 = st.columns(2)
with col1:
    input1 = st.text_input("Ticker 1", value="PETR4")
    weight1 = st.number_input("Weight 1 (%)", min_value=0, max_value=100, value=50) / 100
with col2:
    input2 = st.text_input("Ticker 2", value="VALE3")
    weight2 = st.number_input("Weight 2 (%)", min_value=0, max_value=100, value=50) / 100


if st.button("🔍 Analyze"):
    try:
        end_date = time.strftime("%Y-%m-%d")
        start_date = f"{int(time.strftime('%Y'))-5}-01-01"
        tickers = [f"{input1}.SA", f"{input2}.SA"]
        data = Ticker(tickers).history(start=start_date, end=end_date)

        if data.empty:
            st.error("Nenhum dado encontrado. Verifique os tickers.")
        else:
            df = data.reset_index()

            df_roi_list = []
            for ticker in tickers:
                temp_df = df[df["symbol"] == ticker].copy()
                temp_df["ROI"] = temp_df["close"] / temp_df["close"].iloc[0] * 100
                df_roi_list.append(temp_df[["date", "symbol", "ROI"]])

            df_roi = pd.concat(df_roi_list)
            df_roi["date"] = pd.to_datetime(df_roi["date"])

            merged = pd.merge(
                df[df["symbol"] == tickers[0]][["date", "close"]],
                df[df["symbol"] == tickers[1]][["date", "close"]],
                on="date",
                suffixes=(f"_{tickers[0]}", f"_{tickers[1]}")
            )

            merged["ret1"] = merged[f"close_{tickers[0]}"].pct_change()
            merged["ret2"] = merged[f"close_{tickers[1]}"].pct_change()

            merged["portfolio_ret"] = merged["ret1"] * weight1 + merged["ret2"] * weight2
            annual_return = (1 + merged["portfolio_ret"].mean()) ** 250 - 1

            col1, col2 = st.columns(2)
            with col1:
                plt.figure(figsize=(6, 4))
                sns.lineplot(data=df_roi, x="date", y="ROI", hue="symbol")
                plt.title("5Y Cumulative ROI")
                plt.tight_layout()
                st.pyplot(plt.gcf())

            with col2:
                ytd = df_roi[df_roi["date"] >= pd.to_datetime(f"{time.strftime('%Y')}-01-01")]
                plt.figure(figsize=(6, 4))
                sns.lineplot(data=ytd, x="date", y="ROI", hue="symbol")
                plt.title("YTD Cumulative ROI")
                plt.tight_layout()
                st.pyplot(plt.gcf())

            st.metric("📊 Retorno Anualizado da Carteira", f"{annual_return * 100:.2f}%")

    except Exception as e:
        st.error(f"Erro ao buscar os dados: {e}")
