import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from scipy.stats import iqr



monthly_aggregated = pd.read_csv('arima_aggregated_forecast.csv',sep=',')
plt.rc('font', size=8)
print(monthly_aggregated.info())

plt.figure(figsize=(18, 12))

# Predicted Water M3
plt.subplot(3, 2, 1)
plt.bar(monthly_aggregated['Month'], monthly_aggregated['Predicted Water M3'], color='lightblue')
plt.title('Total Water Usage (m³) per Month')
plt.xlabel('Month')
plt.ylabel('Water M3')
plt.xticks(monthly_aggregated['Month'])
plt.grid(axis='y')

# Warm Water M3
plt.subplot(3, 2, 2)
plt.bar(monthly_aggregated['Month'], monthly_aggregated['Warm Water M3'], color='lightcoral')
plt.title('Total Warm Water Usage (m³) per Month')
plt.xlabel('Month')
plt.ylabel('Warm Water M3')
plt.xticks(monthly_aggregated['Month'])
plt.grid(axis='y')

# Total Water Cost per person
plt.subplot(3, 2, 3)
plt.bar(monthly_aggregated['Month'], monthly_aggregated['Total Water Cost per person'], color='lightgreen')
plt.title('Total Water Cost (EUR) per Person per Month')
plt.xlabel('Month')
plt.ylabel('Total Water Cost per Person (EUR)')
plt.xticks(monthly_aggregated['Month'])
plt.grid(axis='y')

# Predicted Heat MWH
plt.subplot(3, 2, 4)
plt.bar(monthly_aggregated['Month'], monthly_aggregated['Predicted Heat MWH'], color='lightyellow')
plt.title('Total Heat Usage (MWH) per Month')
plt.xlabel('Month')
plt.ylabel('Heat MWH')
plt.xticks(monthly_aggregated['Month'])
plt.grid(axis='y')

# Daily Heating Cost
plt.subplot(3, 2, 5)
plt.bar(monthly_aggregated['Month'], monthly_aggregated['Monthly Heating Cost'], color='lightsalmon')
plt.title('Total Heating Cost (EUR) per Month')
plt.xlabel('Month')
plt.ylabel('Heating Cost (EUR)')
plt.xticks(monthly_aggregated['Month'])
plt.grid(axis='y')

plt.tight_layout()
plt.show()

