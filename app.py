import streamlit as st
import pandas as pd
from datetime import datetime

# 1. MOBILE STYLE CSS
st.set_page_config(page_title="Nawed Khata", layout="centered")

st.markdown("""
    <style>
    /* Pure Android/iOS App Look */
    .main { background-color: #F0F4F8; }
    .stApp { max-width: 500px; margin: 0 auto; } /* Mobile View Constrain */
    
    /* Custom Card Style */
    .summary-card {
        background: linear-gradient(135deg, #007AFF, #00C6FF);
        padding: 20px;
        border-radius: 20px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,122,255,0.2);
    }
    
    /* Bottom Navigation Bar Simulation */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 10px 0;
        display: flex;
        justify-content: space-around;
        border-top: 1px solid #ddd;
        z-index: 1000;
    }
    
    /* Big Plus Button */
    .add-btn {
        background-color: #FF3B30;
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE FOR DATA
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Date", "Name", "Item", "Amount", "Mode", "Status", "Profit"])

# 3. NAVIGATION (Using Radio as Tabs)
tab = st.radio("", ["🏠 Home", "📖 Khata", "➕ Add", "📊 Report", "⚙️ Profile"], horizontal=True, label_visibility="collapsed")

st.divider()

# --- 🏠 HOME SCREEN ---
if tab == "🏠 Home":
    st.markdown("""
        <div class="summary-card">
            <p style="margin:0; opacity:0.8;">Total Business (Nawed Enterprises)</p>
            <h1 style="margin:0; font-size:40px;">₹ 45,000</h1>
            <div style="display:flex; justify-content:space-between; margin-top:20px;">
                <div><small>Udhaar 🔴</small><br><b>₹ 12,000</b></div>
                <div><small>Profit 💰</small><br><b>₹ 8,500</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Pichli Entries")
    if not st.session_state.db.empty:
        st.dataframe(st.session_state.db.tail(5), use_container_width=True)
    else:
        st.info("Bhai, aaj koi entry nahi hui!")

# --- ➕ ADD ENTRY SCREEN ---
elif tab == "➕ Add":
    st.title("🎙️ Nayi Entry")
    with st.form("entry_form", clear_on_submit=True):
        name = st.text_input("Grahak ka Naam (Mic use karein)")
        item = st.text_input("Kya Maal Diya?")
        col1, col2 = st.columns(2)
        amt = col1.number_input("Becha (Sale)", min_value=0)
        cost = col2.number_input("Kharid (Cost)", min_value=0)
        mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Udhaar (Pending)"])
        
        if st.form_submit_button("Database mein Save Karein ✅"):
            new_row = pd.DataFrame([{
                "Date": datetime.now().strftime("%d-%m-%Y"),
                "Name": name, "Item": item, "Amount": amt,
                "Mode": mode, "Status": "Unpaid" if "Udhaar" in mode else "Paid",
                "Profit": amt - cost
            }])
            st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
            st.success("Entry Saved!")

# --- 📖 KHATA SCREEN ---
elif tab == "📖 Khata":
    st.title("📖 Grahak Ledger")
    search = st.text_input("🔍 Search Name...")
    # Yahan list dikhegi
    st.warning("Feature Under Construction: Yahan har party ka alag panna khulega.")

# --- 📊 REPORT SCREEN ---
elif tab == "📊 Report":
    st.title("📊 Business Analysis")
    st.write("Aapka munaafa aur sales ka graph yahan dikhega.")

# --- ⚙️ PROFILE SCREEN ---
elif tab == "⚙️ Profile":
    st.title("👤 Settings")
    st.text_input("Shop Name", value="Nawed Enterprises")
    st.button("Logout")
    st.info("Nawed Khata v1.0 (BETA)")
