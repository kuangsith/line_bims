import pandas as pd
from bs4 import BeautifulSoup
import requests
import config
import line_noti
import datetime
import pytz

tablist = config.tablist()
unit_dict = config.unit_dict()

msg = "Water Report\n"

bangkok_tz = pytz.timezone('Asia/Bangkok')
now_utc = datetime.datetime.now(pytz.utc)
now_bangkok = now_utc.astimezone(bangkok_tz)
day_before = now_bangkok - datetime.timedelta(days=1)

run_date = now_bangkok.strftime(format="%Y-%m-%d")
# run_date = '2024-06-13' #Uncomment here to override

date_end = run_date
date_start = ((datetime.datetime.strptime(date_end,"%Y-%m-%d")) + datetime.timedelta(days=-1)).strftime(format = "%Y-%m-%d")
msg += f"Run Date: {run_date}\n"

msg += "-"*24 +"\n"

for tabname in tablist:

    msg += f"Data from table {tabname}\n"

    url = f'http://110.49.150.135:4002/CPU/?command=DataQuery&uri=dl:tabACTW&format=html&mode=date-range&p1={date_start}T18:00:00&p2={date_end}T18:00:00'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all(['td', 'th'])
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    df = pd.DataFrame(data[1:],columns=data[0])

    

    collist= [col for col in df.columns if col not in ['TimeStamp','Record']]


    df['TimeStamp'] = pd.to_datetime(df['TimeStamp']).dt.tz_localize(bangkok_tz)
 
    msg += f"Number of data points: {df.shape[0]}\n\n"

    for col in collist:
        df[col] = df[col].astype('float')
        msg += f"{col}: {df[col].median():.2f} {unit_dict.get(col) if unit_dict.get(col) is not None else ''}\n"

    msg += "-"*24 + "\n"

line_noti.sendmsg(msg)
# print(msg)

