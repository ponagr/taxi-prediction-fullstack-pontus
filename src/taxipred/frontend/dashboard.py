import streamlit as st


st.set_page_config(layout="wide", page_title="Taxi Prediction Dashboard")

st.title("Page Descriptions")

st.markdown("### Overview Page:")
st.markdown("***Overview of the data used for model training***")

st.markdown("### Customer Page:")
st.markdown("***Selection of date, time, pickup and destination to get and estimated total taxi price for the customer***")

st.markdown("### Company Page:")
st.markdown("***Simple analysis for a taxi company to test different parameters and get expected price outcomes, to get a clearer view of when income is higher or lower***")


# TODO: lägg till rolig bakgrund
# TODO: lägga in datan med missing values på Taxi_Price för att kunna klicka på och fylla värden från dashboarden
# TODO: testa olika modeller för categorical_feature predictions
# TODO: lite plots och metrics
# TODO: fyll missing values med random forest, jämför med tidigare cleaned och original df
# TODO: sida för att se och jämföra datasets, med describe
# TODO: sida för att testa predictions på missing_target_data och fylla dess värden och jämföra dess description värden med originalet
# TODO: fixa till readme



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

