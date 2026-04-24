import streamlit as st
import pandas as pd
from datetime import datetime
import io
import plotly.express as px

# 1. SETUP & THEME
st.set_page_config(page_title="Nawed Enterprises V3 - Super Bundle", layout="wide")

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=[
        "ID", "Date", "Customer", "Item", "Amount", "Cost", "Mode", "Status", "Profit", "Note"
    ])

# SIDEBAR: SETTINGS & PROFILE
with st.sidebar:
    st.title("⚙️ Control Panel")
    lang = st.selectbox("🌐 Choose Language / भाषा चुनें", ["Hindi", "English"])
    st.divider()
    st.subheader("👤 Profile Settings")
    shop_name = st.text_input("Shop Name", "Nawed Enterprises")
    owner = st.text_input("Owner Name", "Nawed Bhai")
    
    st.divider()
    if st.button("🗑️ Reset All Data"):
        st.session_state.db = pd.DataFrame(columns=["ID", "Date", "Customer", "Item", "Amount", "Cost", "Mode", "Status", "Profit", "Note"])
        st.rerun()

# 2. TRANSLATIONS (HINDI/ENGLISH)
text = {
    "Hindi": {
        "title": f"🚀 {shop_name} डिजिटल मैनेजर",
        "welcome": f"स्वागत है, {owner}",
        "entry_h": "🎙️ नयी एंट्री (Voice Support)",
        "save_btn": "डाटा सेव करें ✅",
        "dash_h": "📊 आज का व्यापार",
        "search_h": "🔍 खोजें और उधार वसूलें",
        "profit_h": "📈 मुनाफे का विश्लेषण",
        "export": "📥 एक्सेल रिपोर्ट डाउनलोड करें",
        "warning": "⚠️ ध्यान दें: आप नुकसान में बेच रहे हैं!"
    },
    "English": {
        "title": f"🚀 {shop_name} Digital Manager",
        "welcome": f"Welcome, {owner}",
        "entry_h": "🎙️ New Entry (Voice Support)",
        "save_btn": "Save Transaction ✅",
        "dash_h": "📊 Business Dashboard",
        "search_h": "🔍 Search & Recover Payment",
        "profit_h": "📈 Profit Analytics",
        "export": "📥 Download Excel Report",
        "warning": "⚠️ Warning: You are selling at a loss!"
    }
}
t = text[lang]

# 3. DASHBOARD METRICS
st.title(t["title"])
st.write(f"📅 {datetime.now().strftime('%d-%m-%Y')} | {t['welcome']}")

df = st.session_state.db
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Sales", f"₹{df['Amount'].sum()}")
with c2:
    pending = df[df['Status'] == 'Unpaid']['Amount'].sum()
    st.metric("Total Udhaar 🔴", f"₹{pending}", delta_color="inverse")
with c3:
    st.metric("Net Profit 💰", f"₹{df['Profit'].sum()}")
with c4:
    st.metric("Total Parties", len(df['Customer'].unique()))

st.divider()

# 4. 25-FEATURE ENTRY SYSTEM
st.header(t["entry_h"])
with st.expander("📝 Fill Transaction Details", expanded=True):
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        cust = st.text_input("Customer Name (Mic 🎙️)")
        item_val = st.text_input("Item / Product Name")
    with col_b:
        s_price = st.number_input("Selling Price", min_value=0)
        c_price = st.number_input("Cost Price", min_value=0)
    with col_c:
        mode_val = st.selectbox("Payment Mode", ["Cash", "UPI", "Pending"])
        note_val = st.text_input("Extra Note / ID")

    if st.button(t["save_btn"]):
        if cust and s_price > 0:
            profit_val = s_price - c_price
            if profit_val < 0: st.warning(t["warning"])
            
            new_data = pd.DataFrame([{
                "ID": len(df) + 1,
                "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "Customer": cust, "Item": item_val, "Amount": s_price,
                "Cost": c_price, "Mode": mode_val, 
                "Status": "Unpaid" if mode_val == "Pending" else "Paid",
                "Profit": profit_val, "Note": note_val
            }])
            st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
            st.success("Entry Saved!")
            st.rerun()

# 5. SEARCH & LEDGER
st.header(t["search_h"])
search_q = st.text_input("Search by Name or Item...")
if not df.empty:
    f_df = df[df['Customer'].str.contains(search_q, case=False) | df['Item'].str.contains(search_q, case=False)]
    
    # Udhaar Section
    unpaid = f_df[f_df['Status'] == 'Unpaid']
    if not unpaid.empty:
        for idx, row in unpaid.iterrows():
            ca, cb, cc = st.columns([3, 2, 1])
            ca.error(f"🔴 {row['Customer']}: ₹{row['Amount']}")
            rem_text = f"Hi {row['Customer']}, Reminder from {shop_name}: Pending ₹{row['Amount']} for {row['Item']}."
            cb.code(rem_text, language=None)
            if cc.button("Paid ✅", key=f"pay_{idx}"):
                st.session_state.db.at[idx, 'Status'] = 'Paid'
                st.rerun()

    st.dataframe(f_df, use_container_width=True)

    # 6. ANALYTICS (GRAPHS)
    st.header(t["profit_h"])
    fig = px.pie(df, values='Amount', names='Mode', title='Sales by Mode (Cash/UPI/Pending)')
    st.plotly_chart(fig, use_container_width=True)

    # 7. EXCEL EXPORT
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales')
    st.download_button(t["export"], data=output.getvalue(), file_name=f"{shop_name}_Report.xlsx")
else:
    st.info("No data yet!")
