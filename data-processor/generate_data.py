'''
MIT License

Greetings! To generate the data used by the globe just run this python file.
If you're confused about the directory structure, you should probably just
refrence the GitHub repository.
'''

import pandas as pd
import json

# I use this as a sanity check to see if everything worked at the end
totals = {'cases': 0}

# Data source should be in here 
df = pd.read_csv('data.csv')

dates = list(df.columns[5:].fillna(0))
locations = list(df['Country/Region'])
latitudes = list(df['Lat'])
longitudes = list(df['Long'])

times = []
compiled = []

# I use this as a sanity check to see if everything worked at the end
largest_cases = {'country': '', 'number': 0}

# You might want to consider adjusting this value since American cases are skyrocketing
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
    
    compiled.append(new)
    times.append(date)

with open('../generate.json', 'w') as file:
    json.dump(compiled, file)
    print('Dumped to ../generate.json')

with open('../times.json', 'w') as file:
    json.dump(times, file)
    print('Dumped to ../times.json')

print('Totals: {}'.format(totals))
print('Largest Cases: {}'.format(largest_cases))