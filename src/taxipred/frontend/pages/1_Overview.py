import streamlit as st
import pandas as pd
from taxipred.utils.helpers import read_api_endpoint, post_api_endpoint
from taxipred.utils.constants import IMG_PATH

st.set_page_config(layout="wide", page_title="Overview Page")

st.title("Overview Page")

df = pd.DataFrame(read_api_endpoint("taxi").json())
df_missing_target = pd.DataFrame(read_api_endpoint("/taxi/missing_target").json())
original_df = pd.DataFrame(read_api_endpoint("/taxi/original").json())
    
tab1, tab2, tab3, tab4 = st.tabs(["Test predictions", "Cleaned data", "Missing target data", "Original data"])
with tab1:
    cols = st.columns(2)
    with cols[0]:
        usd_to_sek = 9.40
        index = st.selectbox("Choose data to predict", df_missing_target.index)
        data_to_predict = df_missing_target.iloc[index]
        st.dataframe(data_to_predict)
        button = st.button("Predict")
        if button:
            payload = data_to_predict.drop(columns="Trip_Price").to_dict()
            response = post_api_endpoint(payload, "taxi/predict").json()
            taxi_price = response.get("Predicted_Price")
            st.info(f"Predicted price: {taxi_price:.2f} USD. ({taxi_price*usd_to_sek:.2f} SEK)")
            df_missing_target.loc[index, "Trip_Price"] = taxi_price
            st.markdown("Updated row:")
            st.dataframe(df_missing_target.iloc[index])   
    with cols[1]:
        st.image(IMG_PATH)
with tab2:
    st.markdown("# Cleaned dataframe used for predicting Trip Price")
    st.dataframe(df)

with tab3:
    st.markdown("# Dataframe with missing Trip Price")
    st.dataframe(df_missing_target)

with tab4:
    st.markdown("# Original Dataframe")
    st.dataframe(original_df)
