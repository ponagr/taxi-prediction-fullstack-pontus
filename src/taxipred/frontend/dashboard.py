import streamlit as st
# from taxipred.utils.helpers import read_api_endpoint, post_api_endpoint, autocomplete_addresses, get_travel_route, get_weather
# import pandas as pd
# from taxipred.utils.constants import FEATURE_MODEL_PATH
# import joblib
# import datetime

st.set_page_config(layout="wide", page_title="Taxi Prediction Dashboard")
st.title("Page Descriptions")
st.markdown("### Overview Page:")
st.markdown("***Overview of the data used for model training***")

st.markdown("### Customer Page:")
st.markdown("***Selection of date, time, pickup and destination to get and estimated total taxi price for the customer***")

st.markdown("### Company Page:")
st.markdown("***Simple analysis for a taxi company to test different parameters and get expected price outcomes, to get a clearer view of when income is higher or lower***")


# TODO: lägg till rolig bakgrund
# TODO: flytta över kod till funktioner
# # TODO: lägga in datan med missing values på Taxi_Price för att kunna klicka på och fylla värden från dashboarden
# TODO: skapa sida för att testa predictions på missing_target_data och fylla dess värden
# # TODO: 4 hours, ta bort hours, och gör 4*60 för att göra till minuter, plussa med mins, gör detta för duration och duration_in traffic
# # TODO: lägg till gräns för datum
# # TODO: testa olika modeller för categorical_feature predictions
# # TODO: ta bort min och max värden i validering?

# def main():
#     st.markdown("# Taxi Prediction Dashboard")

#     st.dataframe(df)
#     st.markdown("# Predict taxi price")

#     with st.form("Taxi fare data"):
#         # konverterar fram och tillbaka direkt i dashboard
#         # för att slippa ändra mer i data cleaning och träna om modell på nya datan 
#         # och ändra alla min och max värden i pydantic och dashboarden
#         usd_to_sek = 9.40   # 1 usd = 9.40 kr
#         sek_to_usd = 1 / usd_to_sek   
        
#         Passenger_Count = st.number_input("Number of passengers", min_value=1.0, max_value=4.0, value=2.0, step=1.0)
        
#         Base_Fare = st.number_input("Base fare (SEK)", min_value=2.0*usd_to_sek, max_value=5.0*usd_to_sek, value=3.5*usd_to_sek, step=0.1)*sek_to_usd
        
#         Per_Km_Rate = st.number_input("Km rate (SEK)", min_value=0.5*usd_to_sek, max_value=2.0*usd_to_sek, value=1.2*usd_to_sek, step=0.1)*sek_to_usd
        
#         Trip_Distance_km = st.number_input("Trip distance (km)", min_value=1.2, max_value=50.0, value=20.0, step=0.1)
        
#         Per_Minute_Rate = st.number_input("Minute rate (SEK)", min_value=0.1*usd_to_sek, max_value=0.5*usd_to_sek, value=0.29*usd_to_sek, step=0.01)*sek_to_usd
        
#         Trip_Duration_Minutes = st.number_input("Trip duration (minutes)", min_value=5.0, max_value=120.0, value=50.0, step=1.0)


#         submitted = st.form_submit_button("PREDICT")

#     if submitted:
#         payload = {
#             "Trip_Distance_km": float(Trip_Distance_km),
#             "Passenger_Count": float(Passenger_Count),
#             "Base_Fare": float(Base_Fare),
#             "Per_Km_Rate": float(Per_Km_Rate),
#             "Per_Minute_Rate": float(Per_Minute_Rate),
#             "Trip_Duration_Minutes": float(Trip_Duration_Minutes),
#         }
#         response = post_api_endpoint(payload, "taxi/predict").json()
#         taxi_price = response.get("Predicted_Price")*usd_to_sek
#         st.markdown(f"Predicted taxi price is {taxi_price:.2f} SEK")
        
        

# 
# # Jämför denna med originalet och lägg till den fyllda missing_target_datan och kolla om dess mean/median ser likadan ut




# # TODO: lite plots och metrics

# # Sida för "kund"
# def test():
#     # karta här för att hitta adresser?
#     cols = st.columns(3)
    
#     with cols[0]:
#         # välj dag
#         day = st.date_input("Day")
        
#         # välj upphämntningstid
#         time = st.time_input("Pickup time")
        
#         Passenger_Count = st.slider("Number of passengers", min_value=1, max_value=4, value=2, step=1)

#         pickup_datetime = datetime.datetime.combine(day, time)
#         pickup_timestamp = int(pickup_datetime.timestamp())
        
            
#     with cols[1]:
#         # välj upphämntningsplats
#         pickup_query = st.text_input("Search pickup adress") 

#         pickup_addresses = autocomplete_addresses(pickup_query)
#         pickup = st.selectbox("Choose pickup adress", pickup_addresses)

#     with cols[2]:
#         # välj avlämningsplats
#         dropoff_query = st.text_input("Search drop off adress")

#         dropoff_addresses = autocomplete_addresses(dropoff_query)
#         dropoff = st.selectbox("Choose drop off adress", dropoff_addresses)
    
    
#     if pickup and dropoff:
        
#         distance, normal_duration, duration, traffic, end_address = get_travel_route(pickup, dropoff, pickup_timestamp)
#         weather = get_weather(pickup_timestamp, end_address)

#         payload = {
#             "Time_of_Day_Evening": 1 if 18 < time.hour < 24 else 0,
#             "Time_of_Day_Morning": 1 if 6 < time.hour < 12 else 0,
#             "Time_of_Day_Night": 1 if time.hour < 6 else 0,
#             "Day_of_Week_Weekend": 0 if day.isoweekday() < 6 else 1,
#             "Traffic_Conditions_Low": 1 if traffic == "Low" else 0,     
#             "Traffic_Conditions_Medium": 1 if traffic == "Medium" else 0,
#             "Weather_Rain": 1 if weather == "Rain" else 0,
#             "Weather_Snow": 1 if weather == "Snow" else 0
#         }
#         # predicta med denna payload, skriv sedan ut priser osv med nästa prediction
#         response = post_api_endpoint(payload, "taxi/fares/predict").json()
#         Base_Fare = response.get("Base_Fare")
#         Per_Km_Rate = response.get("Per_Km_Rate")
#         Per_Minute_Rate = response.get("Per_Minute_Rate")
        
#         if Base_Fare and Per_Km_Rate and Per_Minute_Rate:
            
#             # skicka in payload med predicted base_fare, km_rate och minute_rate till nästa model
#             payload = {
#                 "Trip_Distance_km": float(distance),
#                 "Passenger_Count": float(Passenger_Count),
#                 "Base_Fare": float(Base_Fare),
#                 "Per_Km_Rate": float(Per_Km_Rate),
#                 "Per_Minute_Rate": float(Per_Minute_Rate),
#                 "Trip_Duration_Minutes": float(duration),
#             }
#             response = post_api_endpoint(payload, "taxi/predict").json()
#             usd_to_sek = 9.40   # 1 usd = 9.40 kr
#             taxi_price = response.get("Predicted_Price")*usd_to_sek
            
#             # lite kontroll och jämförelser
#             base_fare_sek = round(Base_Fare*usd_to_sek, 2)
#             km_rate_sek = round(Per_Km_Rate*usd_to_sek, 2)
#             minute_rate_sek = round(Per_Minute_Rate*usd_to_sek, 2)
            
#             distance_price_sek = round((Per_Km_Rate*distance)*usd_to_sek, 2)
#             duration_price_sek = round((Per_Minute_Rate*duration)*usd_to_sek, 2)
#             calculated_price = base_fare_sek+distance_price_sek+duration_price_sek
            
#             st.markdown(f"{base_fare_sek= } | {km_rate_sek= } | {minute_rate_sek= } ")
#             st.markdown(f"{distance= } | {duration= } | {normal_duration= }")
#             st.markdown(f"{weather= } | {traffic= }")
#             st.markdown(f"{distance_price_sek= } | {duration_price_sek= }")
#             st.markdown(f"{calculated_price= }")
#             st.markdown(f"Predicted taxi price is {taxi_price:.2f} SEK")
            
#             # TODO: visa karta med rutt tillsammans med predicted price efter prediction
        
        

    
        

    
    
    
#     # with st.form("Taxi fare data"):
#     #     # konverterar fram och tillbaka direkt i dashboard
#     #     # för att slippa ändra mer i data cleaning och träna om modell på nya datan 
#     #     # och ändra alla min och max värden i pydantic och dashboarden
#     #     usd_to_sek = 9.40   # 1 usd = 9.40 kr
#     #     sek_to_usd = 1 / usd_to_sek   
        
#     #     # Time_of_Day_Evening, Time_of_Day_Morning, Time_of_Day_Night = st.checkbox()
#     #     # Time_of_Day_Evening	Time_of_Day_Morning	Time_of_Day_Night	Day_of_Week_Weekend	Traffic_Conditions_Low	Traffic_Conditions_Medium	Weather_Rain	Weather_Snow
        
#     #     # Time_of_Day based on pickup time
#     #     # 
        
        
#     #     Passenger_Count = st.number_input("Number of passengers", min_value=1, max_value=4, value=2, step=1)
        
#     #     Base_Fare = st.number_input("Base fare (SEK)", min_value=2.0*usd_to_sek, max_value=5.0*usd_to_sek, value=3.5*usd_to_sek, step=0.1)*sek_to_usd
        
#     #     Per_Km_Rate = st.number_input("Km rate (SEK)", min_value=0.5*usd_to_sek, max_value=2.0*usd_to_sek, value=1.2*usd_to_sek, step=0.1)*sek_to_usd
        
#     #     Trip_Distance_km = st.number_input("Trip distance (km)", min_value=1.2, max_value=50.0, value=20.0, step=0.1)
        
#     #     Per_Minute_Rate = st.number_input("Minute rate (SEK)", min_value=0.1*usd_to_sek, max_value=0.5*usd_to_sek, value=0.29*usd_to_sek, step=0.01)*sek_to_usd
        
#     #     Trip_Duration_Minutes = st.number_input("Trip duration (minutes)", min_value=5.0, max_value=120.0, value=50.0, step=1.0)


#     #     submitted = st.form_submit_button("PREDICT")

#     # if submitted:
#     #     payload = {
#     #         "Trip_Distance_km": float(Trip_Distance_km),
#     #         "Passenger_Count": float(Passenger_Count),
#     #         "Base_Fare": float(Base_Fare),
#     #         "Per_Km_Rate": float(Per_Km_Rate),
#     #         "Per_Minute_Rate": float(Per_Minute_Rate),
#     #         "Trip_Duration_Minutes": float(Trip_Duration_Minutes),
#     #     }
#     #     response = taxi_prediction_endpoint(payload).json()
#     #     taxi_price = response.get("Predicted_Price")*usd_to_sek
#     #     st.markdown(f"Predicted taxi price is {taxi_price:.2f} SEK")


# if __name__ == "__main__":
#     test()
#     # main()
