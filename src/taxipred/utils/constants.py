from importlib.resources import files
from dotenv import load_dotenv
import os

# 'files' tar namnet för paketet (vi har satt name="taxipred" i setup.py)
# får tillbaka ett resource-träd med alla filer i paketet (Traversable)
# 'joinpath' skapar sedan en sökväg inne i paketet
# och vår Traversable(resultatet) ser ut såhär: <project-root>/src/taxipred/data/taxi_trip_pricing.csv

# CSV PATHS
# TAXI_ORIGINAL_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv")
TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing_cleaned_no_categorical.csv")
# TAXI_WITH_CATEGORICAL_FEATURES_PATH = files("taxipred").joinpath("data/taxi_trip_pricing_cleaned.csv")
TAXI_MISSING_TARGET_PATH = files("taxipred").joinpath("data/missing_target_data.csv")

# MODEL PATHS
# TAXI_REGRESSOR_MODEL_WITH_CATEGORICAL_FEATURES = files("taxipred").joinpath("models/taxi_regressor_categorical.joblib")
TAXI_MODEL_PATH = files("taxipred").joinpath("models/taxi_regressor.joblib")
FEATURE_MODEL_PATH = files("taxipred").joinpath("models/feature_price_multiregressor.joblib")


# API KEY
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API")
WEATHER_API_KEY = os.getenv("WEATHER_API")
# DATA_PATH = Path(__file__).parents[1] / "data"