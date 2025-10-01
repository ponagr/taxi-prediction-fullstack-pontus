import streamlit as st
from taxipred.utils.helpers import post_api_endpoint

st.set_page_config(layout="wide", page_title="Company Page")

st.title("Company Page")
# TODO: flytta över kod till funktioner
usd_to_sek = 9.40   # 1 usd = 9.40 kr
sek_to_usd = 1 / usd_to_sek   

col1, col2, col3 = st.columns(3)
time = col1.pills("Time of day", ["Morning", "Afternoon", "Evening", "Night"], default="Morning")

day = col2.pills("Day of week", ["Weekday", "Weekend"], default="Weekday")

traffic = col1.pills("Traffic conditions", ["Low", "Medium", "High"], default="Low")

weather = col2.pills("Weather", ["Clear", "Rain", "Snow"], default="Clear")

rates_payload = {
    "Time_of_Day_Evening": 1 if time == "Evening" else 0,
    "Time_of_Day_Morning": 1 if time == "Morning" else 0,
    "Time_of_Day_Night": 1 if time == "Night" else 0,
    "Day_of_Week_Weekend": 0 if day == "Weekday" else 1,
    "Traffic_Conditions_Low": 1 if traffic == "Low" else 0,     
    "Traffic_Conditions_Medium": 1 if traffic == "Medium" else 0,
    "Weather_Rain": 1 if weather == "Rain" else 0,
    "Weather_Snow": 1 if weather == "Snow" else 0
}
        
response = post_api_endpoint(rates_payload, "taxi/fares/predict").json()
Base_Fare = response.get("Base_Fare")
Per_Km_Rate = response.get("Per_Km_Rate")
Per_Minute_Rate = response.get("Per_Minute_Rate")
base_fare_sek = round(Base_Fare*usd_to_sek, 3)
km_rate_sek = round(Per_Km_Rate*usd_to_sek, 3)
minute_rate_sek = round(Per_Minute_Rate*usd_to_sek, 3)


c1,c2 = col1.columns(2)
c1.info(f"Base Fare \n{base_fare_sek}")
c2.info(f"Per Km Rate \n{km_rate_sek}")
c3,c4 = col2.columns(2)
c3.info(f"Per Minute Rate \n{minute_rate_sek}")

Passenger_Count = col1.pills("Number of passengers", [1,2,3,4], default=2)

Trip_Distance_km = col1.slider("Trip distance (km)", min_value=1.2, max_value=50.0, value=20.0, step=0.1)

Trip_Duration_Minutes = col1.slider("Trip duration (minutes)", min_value=5.0, max_value=120.0, value=50.0, step=1.0)


payload = {
    "Trip_Distance_km": float(Trip_Distance_km),
    "Passenger_Count": float(Passenger_Count),
    "Base_Fare": float(Base_Fare),
    "Per_Km_Rate": float(Per_Km_Rate),
    "Per_Minute_Rate": float(Per_Minute_Rate),
    "Trip_Duration_Minutes": float(Trip_Duration_Minutes),
}

response = post_api_endpoint(payload, "taxi/predict").json()
taxi_price = response.get("Predicted_Price")*usd_to_sek
col1.info(f"Predicted Taxi Price: {taxi_price:.2f} SEK")
