from fastapi import FastAPI, UploadFile, File
import pandas as pd
import mlflow
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os, traceback
from forecasting import run_forecast

app = FastAPI()

@app.get("/check/")
async def check(): 
    print("[LOG] Health check endpoint accessed ", flush=True)
    return {"status": "OK"}

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    print("[LOG] Starts", flush=True)
    try:
        print("[LOG] File upload received:", file.filename, flush=True)

        # Save uploaded file
        content = await file.read()
        file_path = f"/fastapi/tmp/{file.filename}"
        os.makedirs("/fastapi/tmp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)
        print("[LOG] File saved to:", file_path, flush=True)

        # Load DataFrame
        df = pd.read_csv(file_path)
        print("[LOG] Data loaded with shape:", df.shape, flush=True)

        # MLflow setup
        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment("ForecastingApp")

        with mlflow.start_run():
            mlflow.log_param("filename", file.filename)
            print("[LOG] Running forecasting function", flush=True)
            model, forecast = run_forecast(df)
            print("[LOG] Forecasting complete", flush=True)

            y_true = df['y'].values
            y_pred = forecast['yhat'][:len(df)].values

            # Log metrics
            mlflow.log_metric("mse", mean_squared_error(y_true, y_pred))
            mlflow.log_metric("rmse", np.sqrt(mean_squared_error(y_true, y_pred)))
            mlflow.log_metric("mae", mean_absolute_error(y_true, y_pred))
            mlflow.log_metric("mape", np.mean(np.abs((y_true - y_pred) / y_true)) * 100)
            mlflow.log_metric("smape", 100 * np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred))))
            mlflow.log_metric("r2_score", r2_score(y_true, y_pred))

            # Save forecast plot
            fig = model.plot(forecast)
            plot_path = "/tmp/forecast.png"
            plt.savefig(plot_path)
            mlflow.log_artifact(plot_path)

        print("[LOG] All steps completed successfully", flush=True)
        return {"status": "Success"}

    except Exception as e:
        print("[ERROR]", str(e), flush=True)
        traceback.print_exc()
        return {"error": str(e)}
