from fastapi import FastAPI
from taxipred.utils.constants import MODEL_PATH
from taxipred.backend.data_processing import TaxiData, PredictionResponse, TaxiInput
import pandas as pd
import joblib

app = FastAPI()

taxi_data = TaxiData()

# TODO: konvertera alla värden från USD till SEK?
# TODO: göra om passenger count till int?
# TODO: lägga in datan med missing values på Taxi_Price för att kunna klicka på och fylla värden från dashboarden
# TODO: lägga till upphämtningsplats och avlämningsplats, koppla till nån api för maps, och automatiskt fylla i uppskattad distance och duration, endast fylla i rate per min/km, base fare och antal passagerare 

@app.get("/taxi/")
async def read_taxi_data():
    return taxi_data.to_json()


@app.post("/taxi/predict", response_model=PredictionResponse)
async def predict_taxi_price(payload: TaxiInput):
    data_to_predict = pd.DataFrame([payload.model_dump()])
    model = joblib.load(MODEL_PATH)
    prediction = model.predict(data_to_predict)
    
    return {"Predicted_Price": prediction[0]}
