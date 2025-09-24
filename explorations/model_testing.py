from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score
import pandas as pd


def randomforest_hyperparameters(X_train, X_val, y_train, y_val):
    estimators = [100, 500, 1000]
    depth = [None, 10, 20]
    splits = [2, 5, 10]
    leafs = [1, 2, 4]

    model_scores = []
    for e in estimators:
        for d in depth:
            for s in splits:
                for l in leafs:
                    model = RandomForestRegressor(n_estimators=e, max_depth=d, min_samples_split=s, min_samples_leaf=l, random_state=42)
                    model.fit(X_train, y_train)
                    
                    y_pred = model.predict(X_val)
                    rmse = root_mean_squared_error(y_val, y_pred)
                    mae = mean_absolute_error(y_val, y_pred)
                    r2 = r2_score(y_val, y_pred)
                    
                    model_scores.append({
                        "n_estimators": e,
                        "max_depth": d,
                        "min_samples_split": s,
                        "min_samples_leaf": l,
                        "mae": mae,
                        "rmse": rmse,
                        "r2_score": r2
                    })
                    
    return pd.DataFrame(model_scores).sort_values(by="rmse").reset_index(drop=True)



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


def test_models(df, target, test_size=0.2,
                models = {
                    "LinearRegression": LinearRegression(),
                    "RandomForestRegressor": RandomForestRegressor(),
                    "KNeighborsRegressor": KNeighborsRegressor(),
                    "XGBRegressor": XGBRegressor(),
                    "RidgeCV": RidgeCV(),
                    "ElasticNetCV": ElasticNetCV()
                    }, 
                scalers = {
                    "StandardScaler": StandardScaler(), 
                    "MinMaxScaler": MinMaxScaler()
                    }):
    
    X, y = df.drop(columns=[target]), df[target]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42)
    
    result = []
    for key, model in models.items():
        for name, scaler in scalers.items():
            scaler.fit(X_train)

            scaled_X_train = scaler.transform(X_train)
            scaled_X_val = scaler.transform(X_val)
            
            if model == KNeighborsRegressor():
                best_k = find_best_k(scaled_X_train, scaled_X_val, y_train, y_val)
                model = KNeighborsRegressor(n_neighbors=best_k)
            
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
            
    for key, model in models.items():
        if model == KNeighborsRegressor():
                best_k = find_best_k(X_train, X_val, y_train, y_val)
                model = KNeighborsRegressor(n_neighbors=best_k)
                
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        
        mae = mean_absolute_error(y_val, y_pred)
        mse = mean_squared_error(y_val, y_pred)
        rmse = root_mean_squared_error(y_val, y_pred)
        
        result.append({
            "model": key,
            "scaler": "No Scaler",
            "mae": mae,
            "mse": mse,
            "rmse": rmse
        })
    
    result_df = pd.DataFrame(result)
    
    return result_df.sort_values(by="rmse").reset_index(drop=True)