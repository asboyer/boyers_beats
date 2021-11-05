import os, json
import pandas as pd
from datetime import datetime

from api import get_uri, get_img

def uri(x):
    x['track_uri'], x['album_uri'] = get_uri(x['trackName'], x['artistName'])
    print(x['trackName'], x['artistName'], end=": ")
    print(x['track_uri'])
    return x

def func(x):
    x['cover_img'] = get_img(x['album_uri'])
    return x

data_card = """
Time: {}
Tracks: {}
Unique tracks: {}
Span of {} days
{} days out of date
"""
# time string
# tracks
# unique_tracks
# days_of_data
# days_out_of_date

data = {}
counter = 0
for file in os.scandir('data'):
    L = json.load(open(file.path, encoding="utf8"))
    for d in L: 
        data[counter] = d
        counter += 1

df = pd.DataFrame(data)

total_hour_float = (df.iloc[3].sum() * 0.001)/(3600)
total_hour_int = int(total_hour_float)
total_hour_leftover = total_hour_float - total_hour_int
minute_float = total_hour_leftover * 60
minute_int = int(minute_float)
minute_leftover = minute_float - minute_int
seconds_float = round((minute_leftover * 60), 2)
time_string = f"{total_hour_int} hours, {minute_int} minutes, and {seconds_float} seconds."

tracks = len(df.columns)
unique_tracks = len(set(df.iloc[2]))

earlier_date = datetime.strptime(df.iloc[0][0].split(" ")[0], "%Y-%m-%d")
later_date = datetime.strptime(df.iloc[0][len(df.columns) - 1].split(" ")[0], "%Y-%m-%d")
days_of_data = (later_date - earlier_date).days
days_out_of_date = (datetime.now() - later_date).days

df = df.T
df['played'] = 1
df = df.groupby('trackName').agg({'msPlayed': 'sum','artistName': 'first', 'played': 'sum'}).reset_index()
df = df.apply(uri, axis=1)
df = df[df.track_uri != '']

df = df.groupby('album_uri').agg({'msPlayed': 'sum', 'played': 'sum'}).reset_index()
df = df.nlargest(101, 'played')
df = df.apply(func, axis=1)
df = df[df.album_uri != 'spotify:album:4cilxJ0KxbAv5nymwkeGis']
final = {}
i = 0
i = 1
for index, row in df.iterrows():
    f = {}
    f['album_uri'] = row['album_uri']
    f['cover_img'] = row['cover_img']
    f['msPlayed'] = row['msPlayed']
    f['played'] = row['played']
    f['rank'] = i
    final[i] = f
    i += 1

with open("test.json", "w") as file:
    json.dump(final, file, indent=4)
    
f = open("output.txt", "w")
f.write(data_card.format(time_string, tracks, unique_tracks, days_of_data, days_out_of_date))