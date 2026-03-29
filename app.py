import streamlit as st
import pandas as pd
from analyzer import parse_whatsapp_chat, compute_scores

st.set_page_config(page_title="WhatsApp Analyzer", layout="wide")

st.title("📊 WhatsApp Group Activity Dashboard")

uploaded_file = st.file_uploader("Upload WhatsApp chat (.txt)")

if uploaded_file:
    with open("temp_chat.txt", "wb") as f:
        f.write(uploaded_file.read())

    df = parse_whatsapp_chat("temp_chat.txt")
    scores = compute_scores(df)

    st.subheader("🏆 Leaderboard")
    st.dataframe(scores)

    st.subheader("📈 Messages per User")
    st.bar_chart(scores.set_index("User")["Messages"])

    top_user = scores.iloc[0]
    st.success(f"Top Active: {top_user['User']} with {top_user['Messages']} messages")

    st.subheader("📌 Insights")
    st.write(f"Total Messages: {len(df)}")
    st.write(f"Total Users: {df['User'].nunique()}")