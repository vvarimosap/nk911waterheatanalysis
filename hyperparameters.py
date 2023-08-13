
import pandas as pd
import itertools
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from scipy.stats import iqr

# Load the dataset
df = pd.read_csv('vesisahko_feb_aug.csv', delimiter=';')
df['Date'] = pd.to_datetime(df['Timestamp'], format='%d.%m.%Y')
df['Heat MWH'] = df['Heat MWH'].str.replace(',', '.').astype(float)
df['Water M3'] = df['Water M3'].str.replace(',', '.').astype(float)

Q1_water = df['Water M3'].quantile(0.25)
Q3_water = df['Water M3'].quantile(0.75)
IQR_water = iqr(df['Water M3'])
water_outliers = (df['Water M3'] < (Q1_water - 1.5 * IQR_water)) | (df['Water M3'] > (Q3_water + 1.5 * IQR_water))
df = df[~water_outliers]

# Plot ACF and PACF
fig, ax = plt.subplots(1, 2, figsize=(16, 4))
plot_acf(df['Water M3'], lags=30, ax=ax[0])
plot_pacf(df['Water M3'], lags=30, ax=ax[1])
plt.tight_layout()
plt.show()

# Grid search for hyperparameters
p = d = q = range(0, 6)
pdq = list(itertools.product(p, d, q))

best_aic = float('inf')
best_pdq = None

for param in pdq:
    try:
        model = ARIMA(df['Water M3'], order=param)
        results = model.fit()
        if results.aic < best_aic:
            best_aic = results.aic
            best_pdq = param
    except:
        continue

print(f"Best ARIMA parameters: {best_pdq} with AIC: {best_aic}")


