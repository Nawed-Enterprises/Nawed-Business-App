import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Nawed Enterprises | Global", layout="wide", initial_sidebar_state="expanded")

# 2. Royal Dark Theme Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .stTextInput > div > div > input {
        background-color: #121212; color: #FFD700; border: 2px solid #00D4FF;
        border-radius: 15px; height: 55px; font-size: 22px;
    }
    div[data-testid="stMetric"] {
        background-color: #111111; border: 1px solid #333; padding: 15px; border-radius: 10px;
    }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 50px; font-weight: bold;
        background-image: linear-gradient(to right, #00C6FF, #0072FF); color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Business Scale Switch
st.sidebar.title("🏢 Business Control")
biz_type = st.sidebar.selectbox("Business Scale", ["Small Scale (Basic)", "Enterprise (GST/Pro)"])
st.sidebar.divider()
st.sidebar.info(f"Mode: {biz_type} Active")

# 4. Top Section: Master Search & Voice Mic
col_search, col_mic = st.columns([9, 1])
with col_search:
    search_q = st.text_input("", placeholder="🔍 Search Anything... (Name, Bill, Date, Product)")
with col_mic:
    st.markdown("<h2 style='text-align: center;'>🎙️</h2>", unsafe_allow_html=True)

# 5. Core Dashboard Metrics
st.markdown("### 📈 Global Turnover")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Revenue", "₹0.00", "+5%")
m2.metric("Net Profit", "₹0.00", "Stable")
m3.metric("Outstanding", "₹0.00", "-2%", delta_color="inverse")
m4.metric("Active Deals", "0", "New")

st.divider()

# 6. Action Center (The Three Power Buttons)
st.markdown("### ⚡ Quick Actions")
act_col1, act_col2, act_col3 = st.columns(3)

with act_col1:
    if st.button("🔴 SALE (Becha)"):
        st.toast("Sale Entry Open")
with act_col2:
    if st.button("🟢 PURCHASE (Kharida)"):
        st.toast("Purchase Entry Open")
with act_col3:
    if st.button("🟡 LEDGER (Hisaab)"):
        st.toast("Loading Full Record...")

# 7. Enterprise Feature (GST) - Jo sirf Enterprise mode mein dikhega
if biz_type == "Enterprise (GST/Pro)":
    st.divider()
    st.markdown("### 📄 Enterprise Tools")
    if st.button("📝 Generate GST Invoice"):
        st.write("GST Billing Module Initializing...")

# 8. Footer Analytics
st.divider()
st.caption("Nawed Enterprises Universal v1.0 | Scaling Your Vision Globally")
