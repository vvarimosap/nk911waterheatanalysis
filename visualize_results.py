import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('arima_aggregated_forecast.csv')
df['Month'] = df['Month'].astype(int)
df = df.round(2)

# Visualizing the dataframe as a table
fig, ax = plt.subplots(figsize=(16, df.shape[0] * 0.5))
ax.axis('off')

# Creating the table with white background and black font
tbl = ax.table(cellText=df.values, colLabels=df.columns, cellLoc = 'center', loc='center', cellColours=[['white']*df.shape[1]]*df.shape[0])
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.auto_set_column_width(col=list(range(len(df.columns))))

plt.show()


