from fastapi import FastAPI
from taxipred.utils.constants import TAXI_MODEL_PATH, FEATURE_MODEL_PATH
from taxipred.backend.data_processing import TaxiData, PredictionResponse, TaxiInput, TaxiFareInput, TaxiFareOutput
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

@app.get("/taxi/original")
async def read_original_taxi_data():
    return taxi_data.original_to_json()

@app.get("/taxi/missing_target")
async def read_missing_target_data():
    return taxi_data.missing_target_to_json()


@app.post("/taxi/predict", response_model=PredictionResponse)
async def predict_taxi_price(payload: TaxiInput):
    data_to_predict = pd.DataFrame([payload.model_dump()])
    model = joblib.load(TAXI_MODEL_PATH)
    prediction = model.predict(data_to_predict)
    
    return {"Predicted_Price": prediction[0]}


@app.post("/taxi/fares/predict", response_model=TaxiFareOutput)
async def predict_taxi_fares(payload: TaxiFareInput):
    data_to_predict = pd.DataFrame([payload.model_dump()])
    model = joblib.load(FEATURE_MODEL_PATH)
    prediction = model.predict(data_to_predict)
    
    return {
        "Base_Fare": prediction[0][0],
        "Per_Km_Rate": prediction[0][1],
        "Per_Minute_Rate": prediction[0][2]
    }
