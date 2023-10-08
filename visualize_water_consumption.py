import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
df = pd.read_csv('vesisahko_feb_aug.csv', delimiter=';')
df['Date'] = pd.to_datetime(df['Timestamp'], format='%d.%m.%Y')
df['Water M3'] = df['Water M3'].str.replace(',', '.').astype(float)

# Plotting (Zoomed In)
plt.figure(figsize=(16, 6))
plt.plot(df['Date'], df['Water M3'], color='tab:red')
plt.ylim(-25, 25)
plt.xlabel('Date')
plt.ylabel('Water M3')
plt.title('Water Consumption Over Time (Zoomed In)')
plt.tight_layout()
plt.grid(True)
#plt.show()


plt.savefig('plots/water_consumption_raw.png')