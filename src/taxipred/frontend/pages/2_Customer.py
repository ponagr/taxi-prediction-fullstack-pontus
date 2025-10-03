import streamlit as st
from taxipred.utils.helpers import post_api_endpoint, autocomplete_addresses, get_travel_route, get_weather, get_map
import datetime

st.set_page_config(layout="wide", page_title="Customer Page")

st.title("Customer Page")

Passenger_Count = st.pills("Number of passengers", [1,2,3,4], default=2)
cols = st.columns(3)
with cols[0]:
    # välj dag
    # sätt gräns för att hålla dig inom ramen för väder api (5 dagar fram, från nu)
    today = datetime.date.today()
    day = st.date_input("Day", min_value=today, max_value=today + datetime.timedelta(days=5))
    
    # välj upphämntningstid
    time = st.time_input("Pickup time")

    pickup_datetime = datetime.datetime.combine(day, time)
    pickup_timestamp = int(pickup_datetime.timestamp())
    
        
with cols[1]:
    # välj upphämntningsplats
    pickup_query = st.text_input("Search pickup address") 

    pickup_addresses = autocomplete_addresses(pickup_query)
    pickup = st.selectbox("Choose pickup address", pickup_addresses)

with cols[2]:
    # välj avlämningsplats
    dropoff_query = st.text_input("Search drop off address")

    dropoff_addresses = autocomplete_addresses(dropoff_query)
    dropoff = st.selectbox("Choose drop off address", dropoff_addresses)

button = st.button("Predict")
if button:
    if pickup and dropoff:
    # fixed parsing of longer trips, but predictions is not accurate outside of the range of data used for training the prediction model:
        # base_fare_sek= 34.76 | km_rate_sek= 12.14 | minute_rate_sek= 3.1
        # distance= 460.0 | duration= 297.0 | normal_duration= 290.0
        # weather= 'Rain' | traffic= 'High'
        # distance_price_sek= 5585.89 | duration_price_sek= 919.32
        # calculated_price= 6539.97
        # Predicted taxi price is 832.29 SEK
    # ingen ide att ta bort Field och gräns för inputvärden från pydantic klasserna, då predictions blir felaktiga
    
        distance, normal_duration, duration, traffic, end_address = get_travel_route(pickup, dropoff, pickup_timestamp)
        weather = get_weather(pickup_timestamp, end_address)

        payload = {
            "Time_of_Day_Evening": 1 if 18 < time.hour < 24 else 0,
            "Time_of_Day_Morning": 1 if 6 < time.hour < 12 else 0,
            "Time_of_Day_Night": 1 if time.hour < 6 else 0,
            "Day_of_Week_Weekend": 0 if day.isoweekday() < 6 else 1,
            "Traffic_Conditions_Low": 1 if traffic == "Low" else 0,     
            "Traffic_Conditions_Medium": 1 if traffic == "Medium" else 0,
            "Weather_Rain": 1 if weather == "Rain" else 0,
            "Weather_Snow": 1 if weather == "Snow" else 0
        }
        # predicta med denna payload, skriv sedan ut priser osv med nästa prediction
        response = post_api_endpoint(payload, "taxi/fares/predict").json()
        Base_Fare = response.get("Base_Fare")
        Per_Km_Rate = response.get("Per_Km_Rate")
        Per_Minute_Rate = response.get("Per_Minute_Rate")
            
        # skicka in payload med predicted base_fare, km_rate och minute_rate till nästa model
        payload = {
            "Trip_Distance_km": float(distance),
            "Passenger_Count": float(Passenger_Count),
            "Base_Fare": float(Base_Fare),
            "Per_Km_Rate": float(Per_Km_Rate),
            "Per_Minute_Rate": float(Per_Minute_Rate),
            "Trip_Duration_Minutes": float(duration),
        }
        # om duration överstiger vad random forest modellen har tränat på
        # använd elasticCV för linear regression för att kunna predicta över detta ändå, även om det blir mindre accurate
        if duration < 5 or distance < 1.2 or duration > 120 or distance > 50:
            response = post_api_endpoint(payload, "taxi/predict/linear").json()
        else:
            response = post_api_endpoint(payload, "taxi/predict").json()
            
        usd_to_sek = 9.40   # 1 usd = 9.40 kr
        prediction = response.get("Predicted_Price")
        if not prediction:
            st.error(f"API returned no prediction: {response}")
        else:
            taxi_price = prediction*usd_to_sek

            # lite kontroll och jämförelser
            base_fare_sek = round(Base_Fare*usd_to_sek, 2)
            km_rate_sek = round(Per_Km_Rate*usd_to_sek, 2)
            minute_rate_sek = round(Per_Minute_Rate*usd_to_sek, 2)
            
            distance_price_sek = round((Per_Km_Rate*distance)*usd_to_sek, 2)
            duration_price_sek = round((Per_Minute_Rate*duration)*usd_to_sek, 2)
            calculated_price = base_fare_sek+distance_price_sek+duration_price_sek
            
            col1, col2 = st.columns(2)
            col2.info(f"Travel distance: {round(distance)} km")
            col2.info(f"Travel time: {round(duration)} min")
            col2.info(f"Predicted taxi price: {taxi_price:.2f} SEK")
            with col2.expander("Backend Info"):
                st.markdown(f"{base_fare_sek= } | {km_rate_sek= } | {minute_rate_sek= } ")
                st.markdown(f"{distance= } | {duration= } | {normal_duration= }")
                st.markdown(f"{weather= } | {traffic= }")
                st.markdown(f"{distance_price_sek= } | {duration_price_sek= }")
                st.markdown(f"{calculated_price= }")
                
            # visa karta med rutt tillsammans med predicted price efter prediction
            with col1:
                st.info(distance, duration)
                map = get_map(pickup, dropoff)
                st.components.v1.html(
                    f'<iframe src="{map}" width="700" height="500" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
                    height=600,
                )
    else:
        st.warning("You need to choose pickup and drop off address first")