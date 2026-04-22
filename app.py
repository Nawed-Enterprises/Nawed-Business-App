import streamlit as st

# Website Setup
st.set_page_config(page_title="Nawed Enterprises", page_icon="🚀")

st.title("🚀 NAWED ENTERPRISES")
st.subheader("Professional Business Dashboard")

# CEO Branding
st.sidebar.title("CEO Dashboard")
st.sidebar.info("User: Nawed\nStatus: Online")

# Simple App Features
option = st.selectbox("Kya check karna hai?", ["Home", "Add Entry", "Daily Report"])

if option == "Home":
    st.write("---")
    st.success("Welcome, CEO Nawed! Aapka business ab cloud par live hai.")
    st.metric(label="Today's Profit", value="Rs. 0.00", delta="Ready")

elif option == "Add Entry":
    st.write("### Nayi Entry Karein")
    name = st.text_input("Item ya Customer ka Naam")
    amt = st.number_input("Rupaye (Rs.)", min_value=0)
    if st.button("Save to Cloud"):
        st.balloons()
        st.success(f"Dunia bhar se koi bhi ab ye dekh sakta hai! {name} saved.")
