
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from scipy.stats import iqr

# Load dataset
df = pd.read_csv('vesisahko_jun_aug.csv',sep=';')
print(df.columns)
df['Timestamp'] = df['Timestamp'].str.replace(',', '.')
df['Date'] = pd.to_datetime(df['Timestamp'],format="%d.%m.%Y")

# Data preprocessing and imputation
df['Heat MWH'] = df['Heat MWH'].str.replace(',', '.').astype(float)
df['Water M3'] = df['Water M3'].str.replace(',', '.').astype(float)
df.fillna(method='ffill', inplace=True)

df.fillna(method='ffill', inplace=True)

# Remove outliers using IQR for both Water and Heat
Q1_water = df['Water M3'].quantile(0.25)
Q3_water = df['Water M3'].quantile(0.75)
IQR_water = iqr(df['Water M3'])
water_outliers = (df['Water M3'] < (Q1_water - 1.5 * IQR_water)) | (df['Water M3'] > (Q3_water + 1.5 * IQR_water))
df = df[~water_outliers]

Q1_heat = df['Heat MWH'].quantile(0.25)
Q3_heat = df['Heat MWH'].quantile(0.75)
IQR_heat = iqr(df['Heat MWH'])
heat_outliers = (df['Heat MWH'] < (Q1_heat - 1.5 * IQR_heat)) | (df['Heat MWH'] > (Q3_heat + 1.5 * IQR_heat))
df = df[~heat_outliers]

# ARIMA forecasting for water consumption - 1,1,1 best
water_model = ARIMA(df['Water M3'], order=(1,1,5))
water_model_fit = water_model.fit()
water_forecast = water_model_fit.forecast(steps=365)

# ARIMA forecasting for heat consumption
heat_model = ARIMA(df['Heat MWH'], order=(0,1,1))
heat_model_fit = heat_model.fit()
heat_forecast = heat_model_fit.forecast(steps=365)

# Combining the forecasts and calculating the costs
forecast_df = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', end='2023-12-31'),
    'Predicted Water M3': water_forecast,
    'Predicted Heat MWH': heat_forecast
})

# Costs calculations
static_percentage = 0.40
water_price_per_m3 = 3.7696
number_of_people = 30
forecast_df['Warm Water M3'] = forecast_df['Predicted Water M3'] * static_percentage
forecast_df['Daily Water Cost'] = forecast_df['Predicted Water M3'] * water_price_per_m3
forecast_df['Warm Heating Water Cost per person'] = forecast_df['Warm Water M3'] * water_price_per_m3 / number_of_people
forecast_df['Cold Water Cost per person'] = forecast_df['Predicted Water M3'] * water_price_per_m3 / number_of_people
forecast_df['Total Water Cost per person'] = forecast_df['Warm Heating Water Cost per person'] + forecast_df['Cold Water Cost per person']

# Adding heating cost based on given monthly rates
heating_prices = {1: 80.6, 2: 80.6, 3: 71.92, 4: 57.04, 5: 42.16, 6: 33.48, 7: 33.48, 8: 33.48, 9: 40.92, 10: 59.52, 11: 69.44, 12: 78.12}
forecast_df['Month'] = forecast_df['Date'].dt.month
forecast_df['Daily Heating Cost'] = forecast_df['Month'].map(heating_prices) * forecast_df['Predicted Heat MWH']

# Aggregate the results on a monthly level
monthly_aggregated = forecast_df.groupby(forecast_df['Date'].dt.month).agg({
    'Predicted Water M3': 'sum',
    'Daily Water Cost': 'sum',
    'Warm Water M3': 'sum',
    'Warm Heating Water Cost per person': 'sum',
    'Cold Water Cost per person': 'sum',
    'Total Water Cost per person': 'sum',
    'Predicted Heat MWH': 'sum',
    'Daily Heating Cost': 'sum'
}).reset_index().rename(columns={'Date': 'Month','Daily Heating Cost':'Monthly Heating Cost','Daily Water Cost':'Monthly Water Cost'})

# Save the final aggregated dataset
monthly_aggregated.to_csv('arima_aggregated_forecast.csv', index=False)

print("Analysis with ARIMA complete. Results saved to 'arima_aggregated_forecast.csv'.")


pd.set_option('display.max_colwidth', None)
print(monthly_aggregated)
