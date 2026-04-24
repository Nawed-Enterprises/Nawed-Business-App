import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. MOBILE STYLE CSS (Pehle Wala Mast Look)
st.set_page_config(page_title="Nawed Khata", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #F0F4F8; }
    .stApp { max-width: 500px; margin: 0 auto; }
    
    .summary-card {
        background: linear-gradient(135deg, #007AFF, #00C6FF);
        padding: 20px;
        border-radius: 20px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,122,255,0.1);
    }
    .num-circle {
        background: rgba(255,255,255,0.2);
        border-radius: 50%; width: 25px; height: 25px;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 14px; margin-right: 5px;
    }
    .stButton>button { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE & DATA
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Date", "Name", "Phone", "Item", "Amount", "Cost", "Mode", "Status", "Profit"])

# 3. LANGUAGE SETTINGS
lang = st.radio("🌐 Language / भाषा", ["Hindi", "English"], horizontal=True)

trans = {
    "English": {
        "home": "🏠 Home", "khata": "📖 Khata", "add": "➕ Add", "report": "📊 Report",
        "sales": "Sales", "udhaar": "Udhaar", "profit": "Profit", "save": "Save Entry",
        "wa_msg": "Hi, your pending balance at Nawed Enterprises is ₹"
    },
    "Hindi": {
        "home": "🏠 होम", "khata": "📖 खाता", "add": "➕ जोड़ें", "report": "📊 रिपोर्ट",
        "sales": "बिक्री", "udhaar": "उधार", "profit": "मुनाफा", "save": "सेव करें",
        "wa_msg": "नमस्ते, Nawed Enterprises में आपका बकाया ₹"
    }
}
t = trans[lang]

# 4. NAVIGATION (Pehle Wala Design)
tab = st.radio("", [t["home"], t["khata"], t["add"], t["report"]], horizontal=True, label_visibility="collapsed")

st.divider()

# --- 🏠 HOME SCREEN (With Numbers 1, 2, 3) ---
if tab == t["home"]:
    sales = st.session_state.db['Amount'].sum()
    udhaar = st.session_state.db[st.session_state.db['Status']=='Unpaid']['Amount'].sum()
    profit = st.session_state.db['Profit'].sum()

    st.markdown(f"""
        <div class="summary-card">
            <p style="margin:0; opacity:0.8;">Nawed Enterprises</p>
            <h1 style="margin:0; font-size:35px;">₹ {sales}</h1>
            <div style="display:flex; justify-content:space-between; margin-top:15px;">
                <div><span class="num-circle">1</span><small>{t['sales']}</small><br><b>₹{sales}</b></div>
                <div><span class="num-circle">2</span><small>{t['udhaar']}</small><br><b>₹{udhaar}</b></div>
                <div><span class="num-circle">3</span><small>{t['profit']}</small><br><b>₹{profit}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader(t["home"])
    st.dataframe(st.session_state.db.tail(5), use_container_width=True)

# --- ➕ ADD ENTRY ---
elif tab == t["add"]:
    st.subheader(t["add"])
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Customer Name")
        phone = st.text_input("Mobile Number (WhatsApp)")
        item = st.text_input("Item")
        c1, c2 = st.columns(2)
        amt = c1.number_input("Sale Price", min_value=0)
        cost = c2.number_input("Cost Price", min_value=0)
        mode = st.selectbox("Mode", ["Cash", "UPI", "Udhaar"])
        if st.form_submit_button(t["save"]):
            new_row = pd.DataFrame([{
                "Date": datetime.now().strftime("%d-%m-%Y"),
                "Name": name, "Phone": phone, "Item": item, "Amount": amt,
                "Cost": cost, "Mode": mode, "Status": "Unpaid" if mode == "Udhaar" else "Paid",
                "Profit": amt - cost
            }])
            st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
            st.success("Success!")

# --- 📖 KHATA (With Edit, Delete, WhatsApp) ---
elif tab == t["khata"]:
    st.subheader(t["khata"])
    search = st.text_input("🔍 Search Name...")
    df = st.session_state.db
    if not df.empty:
        filtered = df[df['Name'].str.contains(search, case=False)]
        for i, row in filtered.iterrows():
            with st.expander(f"👤 {row['Name']} - ₹{row['Amount']}"):
                st.write(f"📅 Date: {row['Date']} | 📦 Item: {row['Item']}")
                
                # WhatsApp Share
                if row['Status'] == 'Unpaid':
                    msg = f"{t['wa_msg']}{row['Amount']} for {row['Item']}."
                    wa_url = f"https://wa.me/91{row['Phone']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f"[📲 Send WhatsApp Reminder]({wa_url})")
                
                # Delete & Edit Buttons
                c1, c2 = st.columns(2)
                if c1.button(f"🗑️ Delete", key=f"del_{i}"):
                    st.session_state.db = st.session_state.db.drop(i)
                    st.rerun()
                if c2.button(f"✅ Mark Paid", key=f"pay_{i}"):
                    st.session_state.db.at[i, 'Status'] = 'Paid'
                    st.rerun()

# --- 📊 MONTHLY REPORT ---
elif tab == t["report"]:
    st.subheader(t["report"])
    df = st.session_state.db
    if not df.empty:
        df['Month'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.strftime('%B %Y')
        monthly = df.groupby('Month').agg({'Amount':'sum', 'Profit':'sum'}).reset_index()
        st.table(monthly)
    else:
        st.info("No data for reports.")
