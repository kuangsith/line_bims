import requests
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pytz
from PIL import Image, ImageEnhance

from google.cloud import bigquery
from google.oauth2 import service_account

# Path to your service account JSON file
service_account_path = "./bims-432306-47663614f7ab.json"

# Load the service account credentials
credentials = service_account.Credentials.from_service_account_file(service_account_path)

# Initialize the BigQuery client
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


bangkok_tz = pytz.timezone('Asia/Bangkok')
now_utc = datetime.datetime.now(pytz.utc)
now_bangkok = now_utc.astimezone(bangkok_tz)
day_before = now_bangkok - datetime.timedelta(days=1)

run_date = now_bangkok.strftime(format="%Y-%m-%d")
# run_date = '2024-06-13' #Uncomment here to override




def get_dat_sensor(tabname,ndays,run_date = run_date):
    date_end = ((datetime.datetime.strptime(run_date,"%Y-%m-%d")) + datetime.timedelta(days=1)).strftime(format = "%Y-%m-%d")
    date_start = ((datetime.datetime.strptime(run_date,"%Y-%m-%d")) + datetime.timedelta(days=-ndays)).strftime(format = "%Y-%m-%d")
    url = f'http://110.49.150.135:4002/CPU/?command=DataQuery&uri=dl:tab{tabname}&format=html&mode=date-range&p1={date_start}T00:00:00&p2={date_end}T00:00:00'
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
    # df['date'] = df['TimeStamp'].dt.date.astype('str')

    for col in collist:
        df[col] = df[col].astype('float')

    return df


def get_dat_gbq(tabname,ndays,run_date=run_date):
    shardlist = []

    # Iterate from start date to end date
    current_date = datetime.datetime.strptime(run_date,'%Y-%m-%d')+ datetime.timedelta(days=-ndays)
    while current_date <= datetime.datetime.strptime(run_date,'%Y-%m-%d'):
        shardlist.append(current_date.strftime('%Y%m%d'))
        current_date += datetime.timedelta(days=1)


    this_df = pd.DataFrame()

    for shard in shardlist:
        
        query = f"""
        SELECT *
        FROM `bims-432306.BIMS_data.{tabname}_raw_{shard}`
        """

        df_temp = client.query(query).to_dataframe()
        this_df = pd.concat([this_df,df_temp])
    # if tabname == 'ACLW':
    #     df_ACLW = this_df.copy()
    #     print(f'Finish Loading {tabname}')
    # if tabname == 'AROW':
    #     df_AROW = this_df.copy()
    #     print(f'Finish Loading {tabname}')
    # if tabname == 'ACTW':
    #     df_ACTW = this_df.copy()
    #     print(f'Finish Loading {tabname}')

    this_df['TimeStamp'] = pd.to_datetime(this_df['TimeStamp'])
    return this_df