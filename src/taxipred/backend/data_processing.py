from taxipred.utils.constants import TAXI_CSV_PATH, TAXI_MISSING_TARGET_PATH, TAXI_ORIGINAL_PATH
import pandas as pd
import json
from pydantic import BaseModel, Field
from typing import Literal


class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(TAXI_CSV_PATH, index_col=0)
        self.missing_target = pd.read_csv(TAXI_MISSING_TARGET_PATH, index_col=0)
        self.df_original = pd.read_csv(TAXI_ORIGINAL_PATH)

    def original_to_json(self):
        return json.loads(self.df_original.to_json(orient="records"))
    
    def missing_target_to_json(self):
        return json.loads(self.missing_target.to_json(orient="records"))
    
    def to_json(self):
        return json.loads(self.df.to_json(orient="records"))


class TaxiInput(BaseModel):
    Trip_Distance_km: float = Field(ge=1.2, le=50)
    Passenger_Count: float = Field(ge=1, le=4)
    Base_Fare: float = Field(ge=2, le=5)
    Per_Km_Rate: float = Field(ge=0.5, le=2)
    Per_Minute_Rate: float = Field(ge=0.1, le=0.5)
    Trip_Duration_Minutes: float = Field(ge=5, le=120)

class TaxiInputElastic(BaseModel):
    Trip_Distance_km: float 
    Passenger_Count: float 
    Base_Fare: float 
    Per_Km_Rate: float 
    Per_Minute_Rate: float
    Trip_Duration_Minutes: float 


class PredictionResponse(BaseModel):
    Predicted_Price: float


class TaxiFareInput(BaseModel):
    Time_of_Day_Evening: int = Literal[0, 1]
    Time_of_Day_Morning: int = Literal[0, 1]
    Time_of_Day_Night: int = Literal[0, 1]
    Day_of_Week_Weekend: int = Literal[0, 1]
    Traffic_Conditions_Low: int = Literal[0, 1]
    Traffic_Conditions_Medium: int = Literal[0, 1]
    Weather_Rain: int = Literal[0, 1]
    Weather_Snow: int = Literal[0, 1]


class TaxiFareOutput(BaseModel):
    Base_Fare: float = Field(ge=2, le=5)
    Per_Km_Rate: float = Field(ge=0.5, le=2)
    Per_Minute_Rate: float = Field(ge=0.1, le=0.5)