import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. Initialization & Settings
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Date", "Name", "Item", "Amount", "Mode", "Status", "Profit"])

# Sidebar for Profile & Language
with st.sidebar:
    st.title("⚙️ Settings")
    lang = st.selectbox("Bhasha / Language", ["English", "Hindi"])
    
    st.divider()
    st.subheader("👤 Profile Setting")
    shop_name = st.text_input("Dukan ka Naam", "Nawed Enterprises")
    owner_name = st.text_input("Malik ka Naam", "Nawed Bhai")
    
    st.info(f"App Version: 2.0 (Premium)")

# Translations
t = {
    "English": {
        "title": f"🚀 {shop_name} Super-App",
        "entry": "Add New Entry",
        "name": "Customer Name",
        "amt": "Amount",
        "save": "Save Entry",
        "history": "Business History",
        "udhaar": "Pending Payments",
        "profit": "Net Profit"
    },
    "Hindi": {
        "title": f"🚀 {shop_name} सुपर-ऐप",
        "entry": "नयी एंट्री जोड़ें",
        "name": "ग्राहक का नाम",
        "amt": "रकम (पैसे)",
        "save": "एंट्री सेव करें",
        "history": "लेन-देन का इतिहास",
        "udhaar": "उधार की लिस्ट",
        "profit": "कुल मुनाफा"
    }
}

curr = t[lang]

# Main UI
st.title(curr["title"])
st.write(f"Welcome, {owner_name} | {datetime.now().strftime('%d-%m-%Y')}")

# --- DASHBOARD ---
df = st.session_state.db
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(curr["amt"], f"₹{df['Amount'].sum()}")
with col2:
    pending = df[df['Status']=='Unpaid']['Amount'].sum()
    st.metric(curr["udhaar"], f"₹{pending}", delta_color="inverse")
with col3:
    st.metric(curr["profit"], f"₹{df['Profit'].sum()}")

st.divider()

# --- ENTRY SECTION ---
st.header(f"🎙️ {curr['entry']}")
with st.container():
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        u_name = st.text_input(curr["name"])
    with c2:
        u_amt = st.number_input("Selling Price", min_value=0)
    with c3:
        u_cost = st.number_input("Cost Price", min_value=0)
    
    u_mode = st.radio("Mode", ["Cash", "UPI", "Pending"], horizontal=True)

    if st.button(curr["save"]):
        if u_name and u_amt > 0:
            new_data = pd.DataFrame([{
                "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "Name": u_name, "Amount": u_amt, "Mode": u_mode,
                "Status": "Unpaid" if u_mode == "Pending" else "Paid",
                "Profit": u_amt - u_cost
            }])
            st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
            st.success("Success!")
            st.rerun()

# --- SEARCH & RECOVERY ---
st.header(f"🔍 Search & Recovery")
search = st.text_input("Search...")
if not df.empty:
    f_df = df[df['Name'].str.contains(search, case=False)]
    
    # Udhaar List with Payment Button
    unpaid = f_df[f_df['Status'] == 'Unpaid']
    for idx, row in unpaid.iterrows():
        col_a, col_b = st.columns([4, 1])
        col_a.warning(f"🔴 {row['Name']} - ₹{row['Amount']}")
        if col_b.button("Paid ✅", key=f"p_{idx}"):
            st.session_state.db.at[idx, 'Status'] = 'Paid'
            st.rerun()

    st.subheader(curr["history"])
    st.dataframe(f_df, use_container_width=True)
