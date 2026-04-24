import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. Page Config
st.set_page_config(page_title="Nawed Enterprises Super-App V3", layout="wide")

# 2. Styling (Premium Look)
st.markdown("""
<style>
    .stMetric { background-color: #1e2130; padding: 20px; border-radius: 15px; border-left: 5px solid #00D4FF; }
    .stButton>button { border-radius: 10px; background-color: #00D4FF; color: black; transition: 0.3s; }
    .stButton>button:hover { background-color: #008CBA; color: white; }
    .pending-row { background-color: #441111; padding: 10px; border-radius: 8px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# 3. Database Initialization
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Date", "Name", "Item", "Amount", "Mode", "Status", "Profit_Est"])

# --- DASHBOARD METRICS ---
df = st.session_state.db
st.title("🛡️ Nawed Enterprises: The Ultimate Business Manager")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Business", f"₹{df['Amount'].sum()}")
with m2:
    pending = df[df['Status']=='Unpaid']['Amount'].sum()
    st.metric("Total Udhaar 🔴", f"₹{pending}", delta_color="inverse")
with m3:
    st.metric("Net Collection", f"₹{df[df['Status']=='Paid']['Amount'].sum()}")
with m4:
    st.metric("Happy Customers", len(df['Name'].unique()))

st.divider()

# --- ENTRY SYSTEM (VOICE & SMART) ---
st.header("🎙️ Quick Voice Entry & Stock")
with st.container():
    c1, c2, c3, c4 = st.columns([2,1,1,1])
    with c1:
        name = st.text_input("Customer Name (Mic 🎙️ use karein)")
    with c2:
        item = st.text_input("Maal/Item Name")
    with c3:
        amt = st.number_input("Selling Price", min_value=0)
    with c4:
        cost = st.number_input("Aapki Kharid (For Profit)", min_value=0)

    p_mode = st.radio("Payment Kaise Hua?", ["Cash", "UPI", "Pending (Udhaar)"], horizontal=True)

    if st.button("🚀 Confirm Entry & Save"):
        if name and amt > 0:
            new_entry = pd.DataFrame([{
                "ID": len(df) + 1,
                "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "Name": name, "Item": item, "Amount": amt, 
                "Mode": p_mode, "Status": "Unpaid" if "Pending" in p_mode else "Paid",
                "Profit_Est": amt - cost
            }])
            st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
            st.success(f"✅ Hisab Saved! Profit Estimate: ₹{amt-cost}")
            st.rerun()

st.divider()

# --- SMART SEARCH & SETTLEMENT ---
st.header("🔍 Intelligent Search & Payment Reminder")
search_box = st.text_input("Search Name, Item or Date...")

if not df.empty:
    filtered = df[df['Name'].str.contains(search_box, case=False) | df['Item'].str.contains(search_box, case=False)]
    
    # 🔴 Udhaar Vasooli Table
    undpaid_list = filtered[filtered['Status'] == 'Unpaid']
    if not undpaid_list.empty:
        st.subheader("🔴 Outstanding Udhaar (Vasooli List)")
        for idx, row in undpaid_list.iterrows():
            col_a, col_b, col_c = st.columns([4, 2, 2])
            col_a.markdown(f"**{row['Name']}** owes ₹{row['Amount']} for {row['Item']}")
            
            # Reminder Feature
            reminder_text = f"Hello {row['Name']}, Nawed Enterprises ki taraf se reminder: Aapka ₹{row['Amount']} baki hai. Kripya chuka dein."
            if col_b.button(f"Copy Reminder 📲", key=f"rem_{idx}"):
                st.write(f"Copy this: {reminder_text}")
            
            if col_c.button("Paisa Mil Gaya ✅", key=f"pay_{idx}"):
                st.session_state.db.at[idx, 'Status'] = 'Paid'
                st.rerun()

    # --- HISTORY & ANALYTICS ---
    st.subheader("📊 Full Business History")
    st.dataframe(filtered, use_container_width=True)

    # Export Feature
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Full Report (CSV)", data=csv, file_name=f"Nawed_Report_{datetime.now().date()}.csv")
else:
    st.info("Bhai, abhi koi entry nahi hui hai. Pehli entry karein!")
