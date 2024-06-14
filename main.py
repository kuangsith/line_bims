import pandas as pd
from bs4 import BeautifulSoup
import requests
import config
import line_noti
import datetime
import pytz

tablist = config.tablist()
unit_dict = config.unit_dict()
npoints = config.npoints()

msg = "Water Report\n"

bangkok_tz = pytz.timezone('Asia/Bangkok')
now_utc = datetime.datetime.now(pytz.utc)
now_bangkok = now_utc.astimezone(bangkok_tz)
msg += f"Timestamp: {now_bangkok.strftime(format = '%Y-%m-%d %H:%M:%S')}\n"

msg += "-"*24 +"\n"

for tabname in tablist:

    msg += f"Data from table {tabname}\n\n"

    url = f'http://110.49.150.135:4002/CPU/?command=DataQuery&uri=dl:tab{tabname}&format=html&mode=most-recent&p1={npoints}&p2='
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


    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
    for col in collist:
        df[col] = df[col].astype('float')
        msg += f"{col}: {df[col].mean():.2f} {unit_dict.get(col) if unit_dict.get(col) is not None else ''}\n"

    msg += "-"*24 + "\n"

line_noti.sendmsg(msg)

