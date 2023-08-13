import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from scipy.stats import iqr

df_arima = pd.read_csv('arima_forecast.csv',sep=',')
df_arima['Date'] = pd.to_datetime(df_arima['Date'])

print(df_arima.columns)

df_actual = pd.read_csv('vesisahko_feb_aug.csv',sep=';')
df_actual['Heat MWH'] = df_actual['Heat MWH'].str.replace(',', '.').astype(float)
df_actual['Water M3'] = df_actual['Water M3'].str.replace(',', '.').astype(float)

print(df_actual.columns)

df_actual['Timestamp'] = df_actual['Timestamp'].str.replace(',', '.')
df_actual['Date'] = pd.to_datetime(df_actual['Timestamp'],format="%d.%m.%Y")

df_join = pd.merge(df_actual, df_arima, on="Date")
print (df_join)
exit

# Adjusting to get the predictions for the available dates in the dataset



# Plotting the actual vs predicted values
plt.figure(figsize=(14, 7))
plt.plot(df_actual['Date'], df_actual['Water M3'], color='red', linestyle='dashed', label='Actual')
plt.plot(df_arima['Date'], df_arima['Predicted Water M3'], color='blue', linestyle='dashed', label='Arima')
plt.title('Water M3: Actual vs ARIMA Predictions')
plt.xlabel('Date')
plt.ylabel('Water K3')
plt.legend()
plt.grid(True)
plt.ylim([-25, 25])
plt.show()

