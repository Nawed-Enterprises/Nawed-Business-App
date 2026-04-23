import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Title
st.set_page_config(page_title="Nawed Enterprises - Smart Manager", layout="centered")

st.title("🚀 Nawed Enterprises")
st.subheader("Digital Hisaab-Kitaab & Database")

# Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Form for data entry
with st.form(key="transaction_form"):
    st.write("### Nayi Entry Karein")
    
    date = st.date_input("Tareekh", datetime.now())
    customer = st.text_input("Customer ka Naam")
    amount = st.number_input("Amount (₹)", min_value=0)
    payment_type = st.selectbox("Type", ["Udhaar (Credit)", "Cash", "Online"])
    details = st.text_area("Samaan ki Detail")
    
    submit_button = st.form_submit_button(label="Hisaab Save Karein")

# Logic to save data
if submit_button:
    if customer == "" or amount == 0:
        st.error("Bhai, Naam aur Amount toh daal do!")
    else:
        # Create a new row of data
        new_data = pd.DataFrame([
            {
                "Date": date.strftime("%Y-%m-%d"),
                "Customer_Name": customer,
                "Amount": amount,
                "Type": payment_type,
                "Details": details
            }
        ])
        
        # Get existing data
        existing_data = conn.read(worksheet="Sheet1", usecols=[0,1,2,3,4])
        
        # Add new data to existing
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        
        # Update Google Sheet
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success(f"Mubarak ho! {customer} ka ₹{amount} ka hisaab save ho gaya hai.")
        st.balloons()

# Show recent history
st.divider()
st.write("### Purana Record (History)")
data = conn.read(worksheet="Sheet1")
st.dataframe(data.tail(10)) # Sirf aakhri 10 entry dikhayega
