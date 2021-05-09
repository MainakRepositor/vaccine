import requests
from fake_useragent import UserAgent
import pandas as pd

ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}
pin = '122001'
date = '07-05-2021'
response = requests.get(
    f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}",
    headers=header)
data = response.json()
print(data)
centers = pd.DataFrame(data.get('centers'))
print(centers.columns)
if centers.empty:
    print('DataFrame is empty!')
session_ids = []

for j, row in centers.iterrows():
    session = pd.DataFrame(row['sessions'][0])
    session['center_id'] = centers.loc[j, 'center_id']
    session_ids.append(session)

sessions = pd.concat(session_ids, ignore_index=True)
av_centeres = centers.merge(sessions, on='center_id')
av_centeres.drop(columns=['sessions', 'session_id','lat', 'block_name','long', 'from', 'to'], inplace=True)
print(av_centeres)
# av_centeres.to_csv('test.csv')
# print(av_centeres.columns)
av_centeres = av_centeres[av_centeres['min_age_limit'] == 45]
print(av_centeres)
#av_centeres.to_csv('test.csv')