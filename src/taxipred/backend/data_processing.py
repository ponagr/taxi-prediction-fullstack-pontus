from taxipred.utils.constants import TAXI_CSV_PATH #TAXI_WITH_CATEGORICAL_FEATURES_PATH, TAXI_MISSING_TARGET_PATH, TAXI_ORIGINAL_PATH
import pandas as pd
import json
from pydantic import BaseModel, Field


# TODO: konvertera alla värden från USD till SEK?
# TODO: göra om passenger count till int?
# TODO: lägga in datan med missing values på Taxi_Price för att kunna klicka på och fylla värden från dashboarden
# TODO: lägga till upphämtningsplats och avlämningsplats, koppla till nån api för maps, och automatiskt fylla i uppskattad distance och duration, endast fylla i rate per min/km, base fare och antal passagerare 

class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(TAXI_CSV_PATH, index_col=0)
        # self.df_categorical = pd.read_csv(TAXI_WITH_CATEGORICAL_FEATURES_PATH)
        # self.df_missing_target = pd.read_csv(TAXI_MISSING_TARGET_PATH)
        # self.df_original = pd.read_csv(TAXI_ORIGINAL_PATH)

    def to_json(self):
        return json.loads(self.df.to_json(orient="records"))


class TaxiInput(BaseModel):
    Trip_Distance_km: float = Field(ge=1.2, le=50)
    Passenger_Count: float = Field(ge=1, le=4)
    Base_Fare: float = Field(ge=2, le=5)
    Per_Km_Rate: float = Field(ge=0.5, le=2)
    Per_Minute_Rate: float = Field(ge=0.1, le=0.5)
    Trip_Duration_Minutes: float = Field(ge=5, le=120)


class PredictionResponse(BaseModel):
    Predicted_Price: float