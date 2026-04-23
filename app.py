import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Nawed Enterprises", layout="centered")
st.title("🚀 Nawed Enterprises")

# Google Sheet ID (Aapki nayi sheet ki ID)
SHEET_ID = "1zK55sa5J04Q1uuugOmc522Arpm8aQEA7brko_LSBg_E"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

# Form
with st.form(key="transaction_form"):
    st.write("### Nayi Entry Karein")
    date = st.date_input("Tareekh", datetime.now())
    customer = st.text_input("Customer ka Naam")
    amount = st.number_input("Amount (₹)", min_value=0)
    payment_type = st.selectbox("Type", ["Udhaar", "Cash", "Online"])
    details = st.text_area("Detail")
    submit = st.form_submit_button("Hisaab Save Karein")

if submit:
    if customer and amount > 0:
        st.info("Bhai, data save karne ke liye niche wala link dabaiye (Security ke liye Streamlit ab aise hi save karta hai):")
        
        # Google Form ya direct link ka rasta
        form_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
        st.markdown(f"[👉 Yahan Click karke Sheet mein Entry check karein]({form_url})")
        
        # Abhi ke liye hum sirf Display karenge kyunki direct 'Update' block ho raha hai
        st.success(f"{customer} ka ₹{amount} ka record ready hai!")
    else:
        st.error("Naam aur Amount bhariye!")

st.divider()
st.write("### Purana Record (History)")
try:
    df = pd.read_csv(SHEET_URL)
    st.dataframe(df)
except:
    st.warning("Sheet se connect nahi ho pa raha. Check karein ki Sheet 'Anyone with link' hai ya nahi.")
