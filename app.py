import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. MOBILE LOOK CSS
st.set_page_config(page_title="Nawed Khata", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #F0F4F8; }
    .stApp { max-width: 500px; margin: 0 auto; }
    .summary-card {
        background: linear-gradient(135deg, #007AFF, #00C6FF);
        padding: 20px; border-radius: 20px; color: white;
        margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,122,255,0.1);
    }
    .num-circle {
        background: rgba(255,255,255,0.2);
        border-radius: 50%; width: 22px; height: 22px;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 12px; margin-right: 5px;
    }
    .metric-box { text-align: center; flex: 1; }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Date", "Name", "Phone", "Item", "Amount", "Cost", "Mode", "Status", "Profit"])
if 'shop_name' not in st.session_state:
    st.session_state.shop_name = "Nawed Enterprises"
if 'lang' not in st.session_state:
    st.session_state.lang = "Hindi"

trans = {
    "English": {
        "home": "🏠 Home", "khata": "📖 Khata", "add": "➕ Add", "report": "📊 Report", "set": "⚙️ Settings",
        "sales": "Sales", "udhaar": "Pending", "profit": "Profit", "save": "Save Entry",
        "wa_msg": "Hi, your pending balance at "
    },
    "Hindi": {
        "home": "🏠 होम", "khata": "📖 खाता", "add": "➕ जोड़ें", "report": "📊 रिपोर्ट", "set": "⚙️ सेटिंग",
        "sales": "बिक्री", "udhaar": "बाकी (Pending)", "profit": "मुनाफा", "save": "सेव करें",
        "wa_msg": "नमस्ते, आपका बकाया "
    }
}
t = trans[st.session_state.lang]

# 3. NAVIGATION TAB
tab = st.radio("", [t["home"], t["khata"], t["add"], t["report"], t["set"]], horizontal=True, label_visibility="collapsed")
st.divider()

# --- 🏠 HOME (Updated with Pending Amount) ---
if tab == t["home"]:
    s = st.session_state.db['Amount'].sum()
    u = st.session_state.db[st.session_state.db['Status']=='Unpaid']['Amount'].sum()
    p = st.session_state.db['Profit'].sum()
    
    st.markdown(f"""
        <div class="summary-card">
            <p style="margin:0; opacity:0.8;">{st.session_state.shop_name}</p>
            <h1 style="margin:0; font-size:35px;">₹ {s}</h1>
            <div style="display:flex; justify-content:space-between; margin-top:20px; gap: 10px;">
                <div class="metric-box">
                    <span class="num-circle">1</span><small>{t['sales']}</small><br><b>₹{s}</b>
                </div>
                <div class="metric-box">
                    <span class="num-circle">2</span><small style="color:#FFDADA;">{t['udhaar']}</small><br><b style="color:#FFDADA;">₹{u}</b>
                </div>
                <div class="metric-box">
                    <span class="num-circle">3</span><small style="color:#D4FFD4;">{t['profit']}</small><br><b style="color:#D4FFD4;">₹{p}</b>
                </div>
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
        phone = st.text_input("Mobile (WhatsApp)")
        item = st.text_input("Item")
        amt = st.number_input("Sale Price", min_value=0)
        cost = st.number_input("Cost Price", min_value=0)
        mode = st.selectbox("Mode", ["Cash", "UPI", "Udhaar"])
        if st.form_submit_button(t["save"]):
            new_row = pd.DataFrame([{
                "Date": datetime.now().strftime("%d-%m-%Y"), "Name": name, "Phone": phone, 
                "Item": item, "Amount": amt, "Cost": cost, "Mode": mode, 
                "Status": "Unpaid" if mode == "Udhaar" else "Paid", "Profit": amt - cost
            }])
            st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
            st.success("Entry Saved!")

# --- 📖 KHATA (WhatsApp, Edit, Delete) ---
elif tab == t["khata"]:
    st.subheader(t["khata"])
    search = st.text_input("🔍 Search Name...")
    df = st.session_state.db
    if not df.empty:
        filtered = df[df['Name'].str.contains(search, case=False)]
        for i, row in filtered.iterrows():
            color = "red" if row['Status'] == 'Unpaid' else "green"
            with st.expander(f"👤 {row['Name']} - ₹{row['Amount']} ({row['Status']})"):
                if row['Status'] == 'Unpaid':
                    msg = f"{t['wa_msg']} {st.session_state.shop_name} is ₹{row['Amount']}."
                    wa_url = f"https://wa.me/91{row['Phone']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f"**[📲 Send WhatsApp Reminder]({wa_url})**")
                
                c1, c2 = st.columns(2)
                if c1.button(f"🗑️ Delete", key=f"del_{i}"):
                    st.session_state.db = st.session_state.db.drop(i)
                    st.rerun()
                if row['Status'] == 'Unpaid':
                    if c2.button(f"✅ Mark Paid", key=f"pay_{i}"):
                        st.session_state.db.at[i, 'Status'] = 'Paid'
                        st.rerun()

# --- 📊 REPORT ---
elif tab == t["report"]:
    st.subheader(t["report"])
    if not st.session_state.db.empty:
        st.write("Full Transaction History")
        st.dataframe(st.session_state.db)
    else:
        st.info("No data available.")

# --- ⚙️ SETTINGS ---
elif tab == t["set"]:
    st.subheader(t["set"])
    st.session_state.shop_name = st.text_input("Shop Name", value=st.session_state.shop_name)
    st.session_state.lang = st.radio("Language / भाषा", ["Hindi", "English"], index=0 if st.session_state.lang=="Hindi" else 1)
    if st.button("🗑️ Clear All Data"):
        st.session_state.db = pd.DataFrame(columns=["Date", "Name", "Phone", "Item", "Amount", "Cost", "Mode", "Status", "Profit"])
        st.rerun()
