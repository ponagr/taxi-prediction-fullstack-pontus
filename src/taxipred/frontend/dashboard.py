import streamlit as st
import streamlit.components.v1 as components
from taxipred.utils.helpers import read_api_endpoint, taxi_prediction_endpoint
import pandas as pd
from taxipred.utils.constants import FEATURE_MODEL_PATH, GOOGLE_MAPS_API_KEY
import joblib
import requests
import datetime

st.set_page_config(layout="wide", page_title="Taxi Prediction Dashboard")

data = read_api_endpoint("taxi")

df = pd.DataFrame(data.json())

# TODO: konvertera alla värden från USD till SEK? - I Dashboard input kanske?
# TODO: göra om passenger count till int?
# TODO: lägga in datan med missing values på Taxi_Price för att kunna klicka på och fylla värden från dashboarden
# TODO: lägga till upphämtningsplats och avlämningsplats, koppla till nån api för maps, och automatiskt fylla i uppskattad distance och duration, endast fylla i rate per min/km, base fare och antal passagerare 
# TODO: kan man träna en modell på att predicta base_fare, per_km_rate och per_minute_rate baserat på dom kategoriska kolumnerna?
# TODO: pydantic model för validering och api call för att predicta base fare, km och min rate
# TODO: bättre att klassificera categorical labels mot base fare, km rate och minute rate istället?

def main():
    st.markdown("# Taxi Prediction Dashboard")

    st.dataframe(df)
    st.markdown("# Predict taxi price")

    with st.form("Taxi fare data"):
        # konverterar fram och tillbaka direkt i dashboard
        # för att slippa ändra mer i data cleaning och träna om modell på nya datan 
        # och ändra alla min och max värden i pydantic och dashboarden
        usd_to_sek = 9.40   # 1 usd = 9.40 kr
        sek_to_usd = 1 / usd_to_sek   
        
        Passenger_Count = st.number_input("Number of passengers", min_value=1.0, max_value=4.0, value=2.0, step=1.0)
        
        Base_Fare = st.number_input("Base fare (SEK)", min_value=2.0*usd_to_sek, max_value=5.0*usd_to_sek, value=3.5*usd_to_sek, step=0.1)*sek_to_usd
        
        Per_Km_Rate = st.number_input("Km rate (SEK)", min_value=0.5*usd_to_sek, max_value=2.0*usd_to_sek, value=1.2*usd_to_sek, step=0.1)*sek_to_usd
        
        Trip_Distance_km = st.number_input("Trip distance (km)", min_value=1.2, max_value=50.0, value=20.0, step=0.1)
        
        Per_Minute_Rate = st.number_input("Minute rate (SEK)", min_value=0.1*usd_to_sek, max_value=0.5*usd_to_sek, value=0.29*usd_to_sek, step=0.01)*sek_to_usd
        
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
        taxi_price = response.get("Predicted_Price")*usd_to_sek
        st.markdown(f"Predicted taxi price is {taxi_price:.2f} SEK")
        
        
def predict_rates():
    model = joblib.load(FEATURE_MODEL_PATH)
    st.time_input()



def test():
    # karta här för att hitta adresser?
    
    cols = st.columns(3)
    
    with cols[0]:
        # välj dag
        day = st.date_input("Day")
        # st.write(day)

        Day_of_Week_Weekend = 1
        if day.isoweekday() < 6:
            Day_of_Week_Weekend = 0
        # st.write(Day_of_Week_Weekend)
        
        # välj upphämntningstid
        time = st.time_input("Pickup time")
        # st.write(time)
        
        Time_of_Day_Evening = 0
        Time_of_Day_Morning = 0
        Time_of_Day_Night = 0
        if 6 < time.hour < 12:
            Time_of_Day_Morning = 1
        if 18 < time.hour < 24:
            Time_of_Day_Evening = 1
        if time.hour < 6:
            Time_of_Day_Night = 1
        # st.write(Time_of_Day_Night, Time_of_Day_Evening, Time_of_Day_Morning)
            
    with cols[1]:
        # välj upphämntningsplats
        query = st.text_input("Search pickup adress") 

        url = (
            f"https://maps.googleapis.com/maps/api/place/autocomplete/json"
            f"?input={query}"
            f"&types=address"
            f"&components=country:se"
            f"&key={GOOGLE_MAPS_API_KEY}"
        )

        response = requests.get(url)
        data = response.json()

        predictions = [p["description"] for p in data.get("predictions", [])]
        pickup = st.selectbox("Choose pickup adress", predictions)

    with cols[2]:
        # välj avlämningsplats
        query2 = st.text_input("Search drop off adress")

        url = (
            f"https://maps.googleapis.com/maps/api/place/autocomplete/json"
            f"?input={query2}"
            f"&types=address"
            f"&components=country:se"
            f"&key={GOOGLE_MAPS_API_KEY}"
        )

        response2 = requests.get(url)
        data = response2.json()

        predictions2 = [p["description"] for p in data.get("predictions", [])]
        dropoff = st.selectbox("Choose drop off adress", predictions2)        

    
    # hämta väder från väder api
    # weather = requests.get()  - skicka med datum och tid?
    
    # lägg till knapp
    # hämta traffic conditions, trip distance och trip duration från maps api
    if pickup and dropoff:
        pickup_datetime = datetime.datetime.combine(day, time)
        departure_timestamp = int(pickup_datetime.timestamp())
        
        # traffic, distance, duration = requests.get()  - skicka med datum och tid?
        response = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={pickup}&destination={dropoff}&departure_time={departure_timestamp}&key={GOOGLE_MAPS_API_KEY}")
        st.write(response.json())
        legs = response.json()["routes"][0]["legs"][0]
        distance = legs["distance"]["text"].strip(" km")
        duration = legs["duration"]["text"].strip(" mins")
        st.write(float(distance), float(duration))
    
        # skicka in payload till model
        
        # payload = {
        #     "Time_of_Day_Evening": 1 if 18 < time.hour < 24 else 0,
        #     "Time_of_Day_Morning": 1 if 6 < time.hour < 12 else 0,
        #     "Time_of_Day_Night": 1 if time.hour < 6 else 0,
        #     "Day_of_Week_Weekend": 0 if day.isoweekday() < 6 else 1,
        #     "Traffic_Conditions_Low": 1 if traffic == "Low" else 0,     # om 
        #     "Traffic_Conditions_Medium": 1 if traffic == "Medium" else 0,
        #     "Weather_Rain": 1 if weather == "Rain" else 0,
        #     "Weather_Snow": 1 if weather == "Snow" else 0
        # }

    
    
    
    with st.form("Taxi fare data"):
        # konverterar fram och tillbaka direkt i dashboard
        # för att slippa ändra mer i data cleaning och träna om modell på nya datan 
        # och ändra alla min och max värden i pydantic och dashboarden
        usd_to_sek = 9.40   # 1 usd = 9.40 kr
        sek_to_usd = 1 / usd_to_sek   
        
        # Time_of_Day_Evening, Time_of_Day_Morning, Time_of_Day_Night = st.checkbox()
        # Time_of_Day_Evening	Time_of_Day_Morning	Time_of_Day_Night	Day_of_Week_Weekend	Traffic_Conditions_Low	Traffic_Conditions_Medium	Weather_Rain	Weather_Snow
        
        # Time_of_Day based on pickup time
        # 
        
        
        Passenger_Count = st.number_input("Number of passengers", min_value=1, max_value=4, value=2, step=1)
        
        Base_Fare = st.number_input("Base fare (SEK)", min_value=2.0*usd_to_sek, max_value=5.0*usd_to_sek, value=3.5*usd_to_sek, step=0.1)*sek_to_usd
        
        Per_Km_Rate = st.number_input("Km rate (SEK)", min_value=0.5*usd_to_sek, max_value=2.0*usd_to_sek, value=1.2*usd_to_sek, step=0.1)*sek_to_usd
        
        Trip_Distance_km = st.number_input("Trip distance (km)", min_value=1.2, max_value=50.0, value=20.0, step=0.1)
        
        Per_Minute_Rate = st.number_input("Minute rate (SEK)", min_value=0.1*usd_to_sek, max_value=0.5*usd_to_sek, value=0.29*usd_to_sek, step=0.01)*sek_to_usd
        
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
        taxi_price = response.get("Predicted_Price")*usd_to_sek
        st.markdown(f"Predicted taxi price is {taxi_price:.2f} SEK")


if __name__ == "__main__":
    test()
    # main()
