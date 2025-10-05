from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score
import pandas as pd
import numpy as np


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
    is_multi = (y_train.ndim > 1 and y_train.shape[1] > 1)
    
    for k in range(1,30):
        test_model = KNeighborsRegressor(n_neighbors=k)
        if is_multi:
            test_model = MultiOutputRegressor(test_model)
        test_model.fit(scaled_X_train, y_train)
        y_pred = test_model.predict(scaled_X_val)
        error = root_mean_squared_error(y_val, y_pred)
        error_list.append(error)

    best_index = np.argmin(error_list)
    best_k = best_index + 1
    
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
    
    
    X, y = df.drop(columns=target), df[target]
    
    if isinstance(y, pd.DataFrame) and y.shape[1] > 1:
        models = {key: MultiOutputRegressor(value) for key, value in models.items()}
        
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42)

    is_multi = (y_train.ndim > 1 and y_train.shape[1] > 1)
    result = []
    
    for model_name, model in models.items():
        base_model = model.estimator if isinstance(model, MultiOutputRegressor) else model
        
        if isinstance(base_model, KNeighborsRegressor):
            best_k = find_best_k(X_train, X_val, y_train, y_val)
            base_model = KNeighborsRegressor(n_neighbors=best_k)
            if isinstance(model, MultiOutputRegressor):
                model = MultiOutputRegressor(base_model)
            else:
                model = base_model
        if is_multi:
            result.append(evaluate_model(model, model_name, "None", X_train, X_val, y_train, y_val, target))
        else:
            result.append(evaluate_model(model, model_name, "None", X_train, X_val, y_train, y_val))
        
        
        for scaler_name, scaler in scalers.items():
            scaler.fit(X_train)

            scaled_X_train = scaler.transform(X_train)
            scaled_X_val = scaler.transform(X_val)
            
            if isinstance(model, KNeighborsRegressor):
                base_model = model.estimator if isinstance(model, MultiOutputRegressor) else model
                if isinstance(base_model, KNeighborsRegressor):
                    best_k = find_best_k(X_train, X_val, y_train, y_val)
                    base_model = KNeighborsRegressor(n_neighbors=best_k)
                    if isinstance(model, MultiOutputRegressor):
                        model = MultiOutputRegressor(base_model)
                    else:
                        model = base_model
        if is_multi:
            result.append(evaluate_model(model, model_name, scaler_name, X_train, X_val, y_train, y_val, target))
        else:            
            result.append(evaluate_model(model, model_name, scaler_name, scaled_X_train, scaled_X_val, y_train, y_val))
            
    # result_df = pd.DataFrame(result)
    
    # return result_df.sort_values(by="rmse").reset_index(drop=True)
    return pd.DataFrame(result)


def evaluate_model(model, model_name, scaler_name, X_train, X_val, y_train, y_val, col_names=None):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        
        # if col_names:
        #     for i, col in enumerate(col_names):
        #         mae = mean_absolute_error(y_val.iloc[:, i], y_pred[:, i])
        #         mse = mean_squared_error(y_val.iloc[:, i], y_pred[:, i])
        #         rmse = root_mean_squared_error(y_val.iloc[:, i], y_pred[:, i])
        #         r2 = r2_score(y_val.iloc[:, i], y_pred[:, i])    
        # else:
        #     mae = mean_absolute_error(y_val, y_pred)
        #     mse = mean_squared_error(y_val, y_pred)
        #     rmse = root_mean_squared_error(y_val, y_pred)
        #     r2 = r2_score(y_val, y_pred)
        
        #     return {"model": model_name, "scaler": scaler_name, "mae": mae, "mse": mse, "rmse": rmse, "r2_score": r2}
        results = {"model": model_name, "scaler": scaler_name}

        if col_names is not None and len(col_names) > 1:
            # Multioutput — lägg till resultat per kolumn
            for i, col in enumerate(col_names):
                mae = mean_absolute_error(y_val.iloc[:, i], y_pred[:, i])
                # mse = mean_squared_error(y_val.iloc[:, i], y_pred[:, i])
                rmse = root_mean_squared_error(y_val.iloc[:, i], y_pred[:, i])
                mean_rmse = rmse/np.abs(y_val.iloc[:, i].mean())
                r2 = r2_score(y_val.iloc[:, i], y_pred[:, i])

                results[f"mae_{col}"] = mae
                # results[f"mse_{col}"] = mse
                results[f"rmse_{col}"] = rmse
                results[f"rmse_%_{col}"] = mean_rmse
                results[f"r2_{col}"] = r2

            # Lägg till genomsnittliga värden över alla targets
            mae_cols = [results[f"mae_{c}"] for c in col_names]
            rmse_cols = [results[f"rmse_{c}"] for c in col_names]
            r2_cols = [results[f"r2_{c}"] for c in col_names]
            results["mae_avg"] = np.mean(mae_cols)
            results["rmse_avg"] = np.mean(rmse_cols)
            results["rmse_%_avg"] = np.mean(mean_rmse)
            results["r2_avg"] = np.mean(r2_cols)

        else:
            # Single output
            mae = mean_absolute_error(y_val, y_pred)
            mse = mean_squared_error(y_val, y_pred)
            rmse = root_mean_squared_error(y_val, y_pred)
            mean_rmse = rmse/np.abs(y_val.mean())
            r2 = r2_score(y_val, y_pred)
            
            results.update({
                "mae": mae,
                "mse": mse,
                "rmse": rmse,
                "rmse_%": mean_rmse,
                "r2_score": r2
            })

        return results