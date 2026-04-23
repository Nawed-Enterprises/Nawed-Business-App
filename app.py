import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Nawed Enterprises", layout="centered")
st.title("🚀 Nawed Enterprises")

# Connection
conn = st.connection("gsheets", type=GSheetsConnection)

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
        new_row = pd.DataFrame([{
            "Date": str(date),
            "Customer_Name": customer,
            "Amount": amount,
            "Type": payment_type,
            "Details": details
        }])
        
        try:
            # Data Read karna
            existing_df = conn.read(worksheet="Sheet1", ttl=0)
            # Naya data jodna
            updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            # SHEET KO UPDATE KARNA (Naya Tareeka)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success(f"Bhai, {customer} ka hisaab save ho gaya!")
            st.balloons()
        except Exception as e:
            # Agar sheet ekdum khali hai toh pehli baar create karega
            conn.update(worksheet="Sheet1", data=new_row)
            st.success("Pehli entry Mubarak ho!")
            st.balloons()
    else:
        st.error("Naam aur Amount bhariye!")

st.divider()
st.write("### Purana Record")
try:
    # ttl=0 ka matlab hai ki har baar taaza data dikhayega
    data = conn.read(worksheet="Sheet1", ttl=0)
    st.dataframe(data)
except:
    st.info("Abhi koi record nahi mila.")
