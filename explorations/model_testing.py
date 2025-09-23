from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error
import pandas as pd

# models = {
#     "LinearRegression": LinearRegression(),
#     "RandomForest": RandomForestRegressor(),
#     "KNN": KNeighborsRegressor(n_neighbors=best_k),
#     "XGBoost": XGBRegressor(),
#     "RidgeCV": RidgeCV(),
#     "ElasticNet": ElasticNetCV()
# }
# scalers = {
#     "StandardScaler": StandardScaler(), 
#     "MinMaxScaler": MinMaxScaler()
#     }

def find_best_k(scaled_X_train, scaled_X_val, y_train, y_val):
    error_list = []
    for k in range(1,30):
        test_model = KNeighborsRegressor(n_neighbors=k)
        test_model.fit(scaled_X_train, y_train)
        y_pred = test_model.predict(scaled_X_val)
        error = root_mean_squared_error(y_val, y_pred)
        error_list.append(error)

    best_index = min(error_list)
    best_k = error_list.index(best_index)+1
    
    return best_k

def test_models(X_train, X_test, X_val, y_train, y_val, models, scalers = {"StandardScaler": StandardScaler(), "MinMaxScaler": MinMaxScaler()}):
    
    result = []
    for key, model in models.items():
        for name, scaler in scalers.items():
            scaler.fit(X_train)

            scaled_X_train = scaler.transform(X_train)
            scaled_X_test = scaler.transform(X_test)
            scaled_X_val = scaler.transform(X_val)
            
            
            best_k = find_best_k(scaled_X_train, scaled_X_val, y_train, y_val)
            
            model.fit(scaled_X_train, y_train)
            y_pred = model.predict(scaled_X_val)
            
            mae = mean_absolute_error(y_val, y_pred)
            mse = mean_squared_error(y_val, y_pred)
            rmse = root_mean_squared_error(y_val, y_pred)
            
            result.append({
                "model": key,
                "scaler": name,
                "mae": mae,
                "mse": mse,
                "rmse": rmse
            })

    result_df = pd.DataFrame(result)
    return result_df.sort_values(by="rmse")