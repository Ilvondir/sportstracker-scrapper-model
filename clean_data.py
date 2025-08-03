import pandas as pd
from pathlib import Path

source = Path('datasets')
data = pd.read_csv(source / 'workouts.csv')

def clean_data(row):
    times = row['Duration'].split(':')
    duration, i = 0, 0
    for time in reversed(times):
        duration += int(time) if i == 0 else int(time) * (60**i)
        i+=1
    row['Duration'] = duration

    row['Distance'] = float(row['Distance'][:-3])
    row['Energy'] = int(row['Energy'][:-5])
    row['Avg. speed'] = float(row['Avg. speed'][:-6])
    row['Max. speed'] = float(row['Max. speed'][:-6])
    row['Steps'] = 0 if pd.isna(row['Steps']) else row['Steps']
    return row

new_data = data.apply(clean_data, axis=1)

new_data.info()
print(new_data.describe())

new_data.to_csv(source / 'cleaned_data.csv', index=False)