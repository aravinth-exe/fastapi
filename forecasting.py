# forecasting.py
import matplotlib
matplotlib.use('Agg')  # use non-GUI backend

from prophet import Prophet

def run_forecast(df):
    print("[LOG] Starting model fitting")
    model = Prophet()
    model.fit(df)
    print("[LOG] Model fitting complete")

    print("[LOG] Predicting future")
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    print("[LOG] Forecast complete")
    return model, forecast