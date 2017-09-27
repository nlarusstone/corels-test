import pandas as pd
import matplotlib.pyplot as plt

time_df = pd.read_csv('../../timing_runs.csv')
time_df.set_index('RunType', inplace=True)
print time_df

for col in time_df.columns:
    time_df.plot(kind='scatter', x=[col] * time_df.shape[1], y=time_df[col])
plt.show()
