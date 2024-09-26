from load_dat import get_dat_gbq, get_dat_sensor
import pytz
import datetime
from datetime import timedelta
import pandas as pd
import config
import warnings
import genimg
import line_noti
warnings.filterwarnings("ignore", category=UserWarning, module="google.cloud.bigquery")


def main(request):
    try:
        tablist = config.tablist()
        unit_dict = config.unit_dict()

        # Get current date in Thailand timezone
        thailand_tz = pytz.timezone('Asia/Bangkok')
        current_thailand_date = datetime.datetime.now(thailand_tz)
        day_before_thailand_date = datetime.datetime.now(thailand_tz) - timedelta(days=1)

        end_date = current_thailand_date.strftime('%Y-%m-%d')
        day_before_date = day_before_thailand_date.strftime('%Y-%m-%d')

        ## Loading Data

        for tabname in tablist:
            df1 = get_dat_sensor(tabname,0,end_date)
            df2 = get_dat_gbq(tabname,6,day_before_date)
            if tabname == 'ACLW':
                df_ACLW = pd.concat([df1,df2])
            if tabname == 'AROW':
                df_AROW = pd.concat([df1,df2])
            if tabname == 'ACTW':
                df_ACTW = pd.concat([df1,df2])

        msg = f"Water Report\n"
        msg += f"Period: {day_before_date} 18:00:00 to {end_date} 18:00:00\n"

        msg += "-"*24 +"\n"

        ## Filter the last day, and generating reporting msg

        for tabname in tablist:

            if tabname == 'ACLW':
                df = df_ACLW.copy()
            if tabname == 'AROW':
                df = df_AROW.copy()
            if tabname == 'ACTW':
                df = df_ACTW.copy()
            
            msg += f"Data from table {tabname}\n"

            df_last24 = df[(df['TimeStamp'] < pd.to_datetime(end_date + " 18:00:00")) & (df['TimeStamp'] > pd.to_datetime(day_before_date + " 18:00:00"))].copy()
        
            msg += f"Number of data points: {df_last24.shape[0]}\n\n"

            collist= [col for col in df_last24.columns if col not in ['TimeStamp','Record']]

            for col in collist:
                df_last24[col] = df_last24[col].astype('float')
                msg += f"{col}: {df_last24[col].median():.2f} {unit_dict.get(col) if unit_dict.get(col) is not None else ''}\n"

            msg += "-"*24 + "\n"
            print(f'Get median for {tabname}')

        genimg.main(df_ACLW,df_ACTW,df_AROW)

        imgurl = line_noti.upload_image_to_imgur('watermark_temp.png')

        line_noti.send_broadcast(msg,imgurl)
    
        return "Success"
    
    except Exception as e:
        return f"Error {str(e)}"

    





    