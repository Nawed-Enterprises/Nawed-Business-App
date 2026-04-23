import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Nawed Enterprises", layout="centered")
st.title("🚀 Nawed Enterprises")

# Connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

# Data Entry Form
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
        new_row = pd.DataFrame([{
            "Date": str(date),
            "Customer_Name": customer,
            "Amount": amount,
            "Type": payment_type,
            "Details": details
        }])
        try:
            # Puraana data lene ki koshish
            df = conn.read(worksheet="Sheet1")
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("Save ho gaya!")
            st.balloons()
        except:
            # Agar sheet khali hai toh naye sire se banaye
            conn.update(worksheet="Sheet1", data=new_row)
            st.success("Pehli entry save ho gayi!")
    else:
        st.error("Naam aur Amount bhariye!")

st.divider()
st.write("### Purana Record")
try:
    data = conn.read(worksheet="Sheet1")
    st.dataframe(data)
except:
    st.info("Abhi tak koi record nahi hai. Pehli entry karein!")
