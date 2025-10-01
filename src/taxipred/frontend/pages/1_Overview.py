import streamlit as st
import pandas as pd
from taxipred.utils.helpers import read_api_endpoint

st.set_page_config(layout="wide", page_title="Overview Page")

st.title("Overview Page")

data = read_api_endpoint("taxi")
df = pd.DataFrame(data.json())

missing_target_data = read_api_endpoint("/taxi/missing_target")
df_missing_target = pd.DataFrame(missing_target_data.json())

original_data = read_api_endpoint("/taxi/original")
original_df = pd.DataFrame(original_data.json())

tab1, tab2, tab3 = st.tabs(["Cleaned data", "Missing target data", "Original data"])

with tab1:
    st.markdown("# Cleaned dataframe used for predicting Trip Price")
    st.dataframe(df)

with tab2:
    st.markdown("# Dataframe with missing Trip Price")
    st.dataframe(df_missing_target)

with tab3:
    st.markdown("# Original Dataframe")
    st.dataframe(original_df)