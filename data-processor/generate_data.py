import pandas as pd
import json

# I use this as a sanity check to see if everything worked at the end
totals = {'cases': 0}

df = pd.read_csv('time_series_covid19_confirmed_global.csv') # Data source should be in here 

dates = list(df.columns[5:].fillna(0))
locations = list(df['Country/Region'])
latitudes = list(df['Lat'])
longitudes = list(df['Long'])

time_selections = []
processed_data = []

# I use this as a sanity check to see if everything worked at the end
largest_cases = {'country': '', 'number': 0}

# You might want to consider adjusting this value since American is suffering from COVID explosion
MAX_CASE = df.iloc[:, -1].max()

for date in dates:
    new = [date, []]
    # Format for the globe: lat, long, number
    all_cases = df[date].fillna(0)

    for i in range(0, len(locations)):
        lat = float(latitudes[i])
        longitude = float(longitudes[i])
        cases = int(all_cases[i])

        new[1].append(lat)
        new[1].append(longitude)
        new[1].append(cases / MAX_CASE)

        if cases > largest_cases['number']:
            largest_cases['number'] = cases
            largest_cases['country'] = df['Country/Region'][i]

        if date == dates[-1]:
            totals['cases'] += cases
    
    processed_data.append(new)
    time_selections.append(date)

with open('../generate.json', 'w') as file:
    json.dump(processed_data, file)
    print('Dumped to ../generate.json')

with open('../time_selections.json', 'w') as file:
    json.dump(time_selections, file)
    print('Dumped to ../time_selections.json')

print('Totals: {}'.format(totals))
print('Largest Cases: {}'.format(largest_cases))