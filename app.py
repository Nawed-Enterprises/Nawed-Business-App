import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Nawed Enterprises", layout="wide")

# 2. Language & Session State
if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

# Language Dictionary
texts = {
    'English': {
        'welcome': "Nawed Enterprises",
        'search': "🔍 Search Anything...",
        'sale': "🔴 SALE",
        'purchase': "🟢 PURCHASE",
        'ledger': "🟡 LEDGER",
        'settings': "⚙️ Settings",
        'profile': "👤 Profile",
        'lang_btn': "Switch to Hindi"
    },
    'Hindi': {
        'welcome': "नावेद एंटरप्राइजेज",
        'search': "🔍 कुछ भी खोजें...",
        'sale': "🔴 बिक्री",
        'purchase': "🟢 खरीदारी",
        'ledger': "🟡 खाता",
        'settings': "⚙️ सेटिंग्स",
        'profile': "👤 प्रोफाइल",
        'lang_btn': "English में बदलें"
    }
}

L = texts[st.session_state.lang]

# 3. Sidebar (Settings & Profile)
with st.sidebar:
    st.title(L['settings'])
    if st.button(L['lang_btn']):
        st.session_state.lang = 'Hindi' if st.session_state.lang == 'English' else 'English'
        st.rerun()
    
    st.divider()
    st.subheader(L['profile'])
    st.text_input("Business Name", "Nawed Enterprises")
    st.text_input("Owner", "Nawed Bhai")
    st.checkbox("Enable GST")
    st.button("Save Profile")

# 4. Main Dashboard UI
st.markdown(f"<h1 style='text-align: center; color: #00D4FF;'>{L['welcome']}</h1>", unsafe_allow_html=True)

# Search Bar
search_q = st.text_input("", placeholder=L['search'])

# Action Buttons
col1, col2, col3 = st.columns(3)
with col1:
    st.button(L['sale'])
with col2:
    st.button(L['purchase'])
with col3:
    st.button(L['ledger'])

st.divider()

# Demo Stats
c1, c2 = st.columns(2)
c1.metric("Today's Business", "₹0.00", "+0%")
c2.metric("Pending Payments", "₹0.00", "0")

st.markdown("---")
st.caption("v1.0 - Ready to Launch")
