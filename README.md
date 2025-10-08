# Labb AI Engineering 1 - taxi predictions

### Project explanation:
Taxi Prediction is a full-stack application that combines machine learning, backend, and frontend to predict taxi fares in real time. 
Through an API layer, the system is scalable, flexible, and easy to integrate with other services. 
The solution helps users make smarter decisions, plan their trips, and avoid unexpected costs. 
For Resekollen AB, the project represents a step toward becoming a complete platform for travel planning and future mobility.

### Dataset:
**Suitable for regression analysis and feature engineering exercises.**
- **Description:**
	- This dataset is designed to predict taxi trip fares based on various factors such as distance, time of day, traffic conditions, and more. It provides realistic synthetic data for regression tasks, offering a unique opportunity to explore pricing trends in the taxi industry.
- **Features:**
	- Distance (in kilometers): The length of the trip.
	- Pickup Time: The starting time of the trip.
	- Dropoff Time: The ending time of the trip.
	- Traffic Condition: Categorical indicator of traffic (light, medium, heavy).
	- Passenger Count: Number of passengers for the trip.
	- Weather Condition: Categorical data for weather (clear, rain, snow).
	- Trip Duration (in minutes): Total trip time.
	- Fare Amount (target): The cost of the trip (in USD).
- **Application:**
	- Predicting taxi fares based on distance, traffic, and weather.

### Data Structure:

```plaintext
taxi-prediction/
│
├── .env                                  # Environment variables (API keys for Google Maps & OpenWeatherMap)
├── requirements.txt                      # Python dependencies required for the project
├── setup.py                              # Installation script for packaging and running the project
├── lab_taxipred.pdf                      # Lab documentation
│
├── explorations/                         # Jupyter notebooks for data exploration, testing & model development
│   ├── model_testing.py                  # Helper file, with functions for testing and evaluating different models on given dataset
│   ├── 1_eda.ipynb                       # Exploratory Data Analysis (EDA)
│   ├── 2_data_cleaning.ipynb             # Data cleaning and preprocessing
│   └── 3_model_exporting.ipynb           # Model training and exporting
│
└── src/
    └── taxipred/
        │
        ├── assets/
        │   └── taxi_img.png              # Dashboard background image
        │
        ├── backend/                      # API and data processing logic
        │   ├── api.py                    # FastAPI endpoints for model predictions
        │   └── data_processing.py        # Pydantic classes for validating data
        │
        ├── data/                         # Local CSV datasets used for model training and testing
        │   ├── cleaned_taxi_data.csv
        │   ├── missing_target_data.csv
        │   ├── taxi_trip_pricing.csv
        │   ├── taxi_trip_pricing_cleaned.csv
        │   └── taxi_trip_pricing_cleaned_categorical.csv
        │
        ├── frontend/                     # Streamlit-based dashboard (UI)
        │   ├── background.py             # Background picture
        │   ├── dashboard.py              # Main Streamlit entry file
        │   └── pages/                    # Streamlit multipage structure
        │       ├── 1_Overview.py         # Overview of data and model testing
        │       ├── 2_Customer.py         # Customer page for predicting taxi prices
        │       └── 3_Company.py          # Company analytics and insights
        │
        ├── models/                       # Saved machine learning models (.joblib)
        │   ├── elastic_regressor.joblib
        │   ├── feature_price_multiregressor.joblib
        │   └── taxi_regressor.joblib
        │
        └── utils/                        # Utility and helper functions
            ├── constants.py              # Global data paths for API-keys, models, csv files etc
            └── helpers.py                # Helper functions for post and get API-requests to different urls
```

## Steps for setting up and running the application:
### Setup
***1. Clone the repository***
```bash
git clone https://github.com/ponagr/taxi-prediction-fullstack-pontus.git
```

***2. Install dependencies***
```bash
uv venv && source venv/Scripts/activate && uv pip install .
```

***3. Get API keys for google maps and openweathermap and setup .env***    
https://developers.google.com/maps    
https://home.openweathermap.org/users/sign_up
```bash
touch .env && echo "WEATHER_API=your_weather_api_key" >> .env && echo "GOOGLE_MAPS_API=your_google_api_key" >> .env
```

### Run application
***Open 2 separate terminals***

***1. Terminal 1 (Backend)***
```bash
cd src/taxipred/backend && uvicorn api:app --reload
```

***2. Terminal 2 (Frontend)***
```bash
cd src/taxipred/frontend && streamlit run dashboard.py
```

## Insights from the EDA, Data Cleaning and Model Selection

During the exploratory and model development phase, I performed extensive testing, comparisons, and evaluations of various models and scalers using multiple datasets (with different imputations and feature sets). To streamline the process, I created helper functions for faster testing and model comparisons.

After several experiments, I decided to use only the numerical features for cleaning and model training, since the categorical features collectively contributed less than 1% to the overall feature importance.

The **RandomForestRegressor** consistently achieved the best performance across all datasets.
The highest accuracy was obtained with the dataset where missing values were **imputed using RandomForestRegressor predictions**, rather than mean or median imputation.

Hyperparameter tuning of the Random Forest model did not yield any significant performance improvements.

For experimentation, I also created a separate **MultiOutput** model to predict **Base Fare** and **Rates per km/minute** using the categorical features. While it doesn’t perform particularly well, it was an interesting exercise to include them in some way.

Lastly, an **ElasticCV** linear regression model was trained to predict prices outside the bounds of the main training data, allowing for more robust extrapolation in rare cases.


