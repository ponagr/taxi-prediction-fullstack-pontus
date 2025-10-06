import streamlit as st
from taxipred.utils.constants import IMG_PATH

st.set_page_config(layout="wide", page_title="Taxi Prediction Dashboard")

cols = st.columns(2)
with cols[0]:
    st.title("Page Descriptions")

    st.markdown("### Overview Page:")
    st.markdown("***Overview of the data used for model training***")

    st.markdown("### Customer Page:")
    st.markdown("***Selection of date, time, pickup and destination to get and estimated total taxi price for the customer***")

    st.markdown("### Company Page:")
    st.markdown("***Simple analysis for a taxi company to test different parameters and get expected price outcomes, to get a clearer view of when income is higher or lower***")
    
with cols[1]:
    st.image(IMG_PATH)