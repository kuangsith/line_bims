import requests
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pytz
from PIL import Image, ImageEnhance

bangkok_tz = pytz.timezone('Asia/Bangkok')
now_utc = datetime.datetime.now(pytz.utc)
now_bangkok = now_utc.astimezone(bangkok_tz)
day_before = now_bangkok - datetime.timedelta(days=1)

run_date = now_bangkok.strftime(format="%Y-%m-%d")
# run_date = '2024-06-13' #Uncomment here to override




def get_dat(tabname,ndays,run_ate = run_date):
    date_end = run_date
    date_start = ((datetime.datetime.strptime(date_end,"%Y-%m-%d")) + datetime.timedelta(days=-ndays)).strftime(format = "%Y-%m-%d")
    url = f'http://110.49.150.135:4002/CPU/?command=DataQuery&uri=dl:tab{tabname}&format=html&mode=date-range&p1={date_start}T00:00:00&p2={date_end}T18:00:00'
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
    df['date'] = df['TimeStamp'].dt.date.astype('str')

    for col in collist:
        df[col] = df[col].astype('float')

    return df

def watermark(imgpath,overlaypath):

    # Opening the primary image (used in background) 
    img1 = Image.open(imgpath) 

    # Opening the secondary image (overlay image) 
    img2 = Image.open(overlaypath)

    # Make img2 50% transparent
    img2 = img2.convert("RGBA")
    alpha = img2.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.05)
    img2.putalpha(alpha)

    # Calculate the position to paste img2 at the center of img1
    img1_width, img1_height = img1.size
    img2_width, img2_height = img2.size
    x = (img1_width - img2_width) // 2
    y = (img1_height - img2_height) // 2

    # Pasting img2 image on top of img1
    img1.paste(img2, (x, y), mask=img2)

    # Displaying the image
    # img1.show()

    output_path = f"./watermark_{imgpath}"
    img1.save(output_path)



def main():
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    ########################################################################################################################################
    df = get_dat('ACLW',6)
    # df = pd.read_pickle('ACLW_temp.pkl')

    col = 'Chlorophyll'

    medians = df.groupby('date')[col].median().reset_index()

    # Step 2: Normalize the medians to the range [0, 1]
    medians['normalized'] = (medians[col] - medians[col].min()) / (medians[col].max() - medians[col].min())

    # Step 3: Create a colormap and map the normalized values to colors
    # cmap = sns.color_palette("coolwarm", as_cmap=True)
    cmap = sns.light_palette("seagreen", as_cmap=True)
    medians['color'] = medians['normalized'].apply(lambda x: cmap(x))

    # Step 4: Create a color mapping dictionary for the dates
    color_dict = dict(zip(medians['date'], medians['color']))

    # Step 5: Plot with the dynamic palette
    ax = sns.boxplot(ax = axs[0,1], x='date', y=col, data=df, width=0.3, showfliers=False, palette=color_dict)

    # Step 6: Add grid lines behind the boxes
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)  # Ensure grid is below the plot elements

    axs[0, 1].hlines(y=5,xmin=-.5,xmax=6.5,color='red',zorder=0)
    axs[0, 1].set_xlabel('Date')
    axs[0, 1].set_ylabel(col)
    axs[0, 1].set_title(f'Boxplot of {col} Grouped by Day')
    axs[0, 1].tick_params(axis='x', rotation=45)
    ########################################################################################################################################

    df = get_dat('ACTW',6)
    # df = pd.read_pickle('ACTW_temp.pkl')

    col = 'Salinity'

    medians = df.groupby('date')[col].median().reset_index()

    # Step 2: Normalize the medians to the range [0, 1]
    medians['normalized'] = (medians[col] - medians[col].min()) / (medians[col].max() - medians[col].min())

    # Step 3: Create a colormap and map the normalized values to colors
    # cmap = sns.color_palette("coolwarm", as_cmap=True)
    cmap = sns.color_palette("coolwarm", as_cmap=True)
    medians['color'] = medians['normalized'].apply(lambda x: cmap(x))

    # Step 4: Create a color mapping dictionary for the dates
    color_dict = dict(zip(medians['date'], medians['color']))

    # Step 5: Plot with the dynamic palette
    ax = sns.boxplot(ax = axs[1,0], x='date', y=col, data=df, width=0.3, showfliers=False, palette=color_dict)

    # Step 6: Add grid lines behind the boxes
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)  # Ensure grid is below the plot elements

    axs[1,0].set_xlabel('Date')
    axs[1,0].set_ylabel(col)
    axs[1,0].set_title(f'Boxplot of {col} Grouped by Day')
    axs[1,0].tick_params(axis='x', rotation=45)

    ########################################################################################################################################
    col = 'WaterTemp_ACTW'

    medians = df.groupby('date')[col].median().reset_index()

    # Step 2: Normalize the medians to the range [0, 1]
    medians['normalized'] = (medians[col] - medians[col].min()) / (medians[col].max() - medians[col].min())

    # Step 3: Create a colormap and map the normalized values to colors
    # cmap = sns.color_palette("coolwarm", as_cmap=True)
    cmap = sns.color_palette("coolwarm", as_cmap=True)
    medians['color'] = medians['normalized'].apply(lambda x: cmap(x))

    # Step 4: Create a color mapping dictionary for the dates
    color_dict = dict(zip(medians['date'], medians['color']))

    # Step 5: Plot with the dynamic palette
    ax = sns.boxplot(ax = axs[0,0], x='date', y=col, data=df, width=0.3, showfliers=False, palette=color_dict)

    # Step 6: Add grid lines behind the boxes
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)  # Ensure grid is below the plot elements


    axs[0,0].set_xlabel('Date')
    axs[0,0].set_ylabel(col)
    axs[0,0].set_title(f'Boxplot of {col} Grouped by Day')
    axs[0,0].tick_params(axis='x', rotation=45)

    ########################################################################################################################################

    df = get_dat('AROW',6)
    # df = pd.read_pickle('AROW_temp.pkl')

    col = 'DO_mgL'

    medians = df.groupby('date')[col].median().reset_index()

    # Step 2: Normalize the medians to the range [0, 1]
    medians['normalized'] = (medians[col] - medians[col].min()) / (medians[col].max() - medians[col].min())

    # Step 3: Create a colormap and map the normalized values to colors
    # cmap = sns.color_palette("coolwarm", as_cmap=True)
    cmap = sns.color_palette("Blues", as_cmap=True)
    medians['color'] = medians['normalized'].apply(lambda x: cmap(x))

    # Step 4: Create a color mapping dictionary for the dates
    color_dict = dict(zip(medians['date'], medians['color']))

    # Step 5: Plot with the dynamic palette
    ax = sns.boxplot(ax = axs[1,1], x='date', y=col, data=df, width=0.3, showfliers=False, palette=color_dict)

    # Step 6: Add grid lines behind the boxes
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)  # Ensure grid is below the plot elements

    axs[1,1].hlines(y=4,xmin=-.5,xmax=6.5,color='red',zorder=0)
    axs[1,1].set_xlabel('Date')
    axs[1,1].set_ylabel(col)
    axs[1,1].set_title(f'Boxplot of {col} Grouped by Day')
    axs[1,1].tick_params(axis='x', rotation=45)


    ########################################################################################################################################

    fig.suptitle(f'Water Quality: Date {run_date}', fontsize=16)
    fig.tight_layout()

    plt.savefig('tempo.png')
    # plt.show()

    watermark('temp.png','./overlay.png')
    





