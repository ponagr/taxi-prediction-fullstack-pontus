# Labb AI Engineering 1 - taxi predictions

### Project explanation:
Taxi Prediction is a full-stack application that combines machine learning, backend, and frontend to predict taxi fares in real time. Through an API layer, the system is scalable, flexible, and easy to integrate with other services. The solution helps users make smarter decisions, plan their trips, and avoid unexpected costs. For Resekollen AB, the project represents a step toward becoming a complete platform for travel planning and future mobility.


## Steps for setting up and running the application:

### Setup
***1. Clone the repository***
```bash
git clone https://github.com/ponagr/taxi-prediction-fullstack-pontus.git
```

***2. Install dependencies***
```bash
uv venv && source venv/Scripts/activate && uv pip install . && uv pip install -r requirements.txt
```

***3. Get API keys for google maps and openweathermap and setup .env***    
https://developers.google.com/maps    
https://home.openweathermap.org/users/sign_up
```bash
touch .env
echo "GOOGLE_MAPS_API=your_google_api_key" > .env
echo "WEATHER_API=your_weather_api_key" > .env
```

***4. Install dependencies***
```bash
uv venv && source venv/Scripts/activate
uv pip install . && uv pip install -r requirements.txt
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

I did a lot of different testing, comparisons, evaluations on different models and scalers with different datasets(different imputations) and columns and comparing the results.

Created functions for easier testing and comparisons of the different models and datasets.

I decided to only use the numerical features and drop the categorical ones for the cleaning and model training, since the categorical features summed together didnt even make up for 1% in the feature_importance.

RandomForestRegressor had best performance for all the datasets.

The best performance was with the dataset where i filled missing values using predictions from RandomForestRegressor instead of using mean/median to fill the values.

No clear performance boost by tuning hyperparameters in the RF model.

Also created a model for predicting Base Fare and Rates for km and minutes based on the categorical features to include and make use of them just for fun, it doesnt perform too well tho.

And an ElasticCV model for linear regression to use for predicting prices outside the bounds of the data used for training.


