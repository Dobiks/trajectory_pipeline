import pandas as pd
import matplotlib.pyplot as plt

df_1 = pd.read_csv('flp_htCym6ABsDxrovAgwKJRei_1.csv')
df_2 = pd.read_csv('flp_htCym6ABsDxrovAgwKJRei.csv')
df_3 = pd.read_csv('flp_htCym6ABsDxrovAgwKJRei_6.csv')

plt.plot(df_1['lat'], df_1['lon'], label='1')
plt.plot(df_2['lat'], df_2['lon'], label='2')
plt.plot(df_3['lat'], df_3['lon'], label='3')
plt.legend()
plt.show()