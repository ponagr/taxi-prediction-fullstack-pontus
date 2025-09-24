import streamlit as st
from taxipred.utils.helpers import read_api_endpoint, taxi_prediction_endpoint
import pandas as pd

st.set_page_config(layout="wide", page_title="Taxi Prediction Dashboard")

data = read_api_endpoint("taxi")

df = pd.DataFrame(data.json())

# TODO: konvertera alla värden från USD till SEK?
# TODO: göra om passenger count till int?
# TODO: lägga in datan med missing values på Taxi_Price för att kunna klicka på och fylla värden från dashboarden
# TODO: lägga till upphämtningsplats och avlämningsplats, koppla till nån api för maps, och automatiskt fylla i uppskattad distance och duration, endast fylla i rate per min/km, base fare och antal passagerare 

def main():
    st.markdown("# Taxi Prediction Dashboard")

    st.dataframe(df)
    st.markdown("# Predict taxi price")

    with st.form("Taxi fare data"):
        Trip_Distance_km = st.number_input("Trip distance (km)", min_value=1.2, max_value=50.0, value=20.0, step=0.1)
        Passenger_Count = st.number_input("Number of passengers", min_value=1.0, max_value=4.0, value=2.0, step=1.0)
        Base_Fare = st.number_input("Base fare", min_value=2.0, max_value=5.0, value=3.5, step=0.1)
        Per_Km_Rate = st.number_input("Km rate", min_value=0.5, max_value=2.0, value=1.2, step=0.01)
        Per_Minute_Rate = st.number_input("Minute rate", min_value=0.1, max_value=0.5, value=0.29, step=0.01)
        Trip_Duration_Minutes = st.number_input("Trip duration (minutes)", min_value=5.0, max_value=120.0, value=50.0, step=1.0)

        submitted = st.form_submit_button("PREDICT")

    if submitted:
        payload = {
            "Trip_Distance_km": float(Trip_Distance_km),
            "Passenger_Count": float(Passenger_Count),
            "Base_Fare": float(Base_Fare),
            "Per_Km_Rate": float(Per_Km_Rate),
            "Per_Minute_Rate": float(Per_Minute_Rate),
            "Trip_Duration_Minutes": float(Trip_Duration_Minutes),
        }
        response = taxi_prediction_endpoint(payload).json()
        taxi_price = response.get("Predicted_Price")
        st.markdown(f"Predicted taxi price is {taxi_price:.2f} USD")


if __name__ == "__main__":
    main()
