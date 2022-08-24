import pygsheets
import datetime as dt
import pandas as pd

# worksheet id
id = 'YOURGOOGLESHEET ID LINK'

# authorization
gc = pygsheets.authorize(service_file='service_account.json')

# setup
sh = gc.open_by_key(id)
wks = sh.sheet1

# Time
tarikh = dt.datetime.now().date()
today = tarikh.strftime('%d/%m/%Y')
tarikh_yes = tarikh - dt.timedelta(days=1)
yesterday = tarikh_yes.strftime('%d/%m/%Y')

# data list
today_data = []
seven_day_list =[]

def display_all():
    wks_result =  wks.get_values('A','D')
    return wks_result

def save_to_csv():
    gsheetpd = pd.DataFrame(display_all())
    gsheetpd.to_csv('fastdata.csv',index=False, header=False)
    print(gsheetpd)

def display_latest():
    wks_result =  wks.get_values('A','D')
    #print (wks_result[-1])
    return wks_result[-1]

def get_specify_date(date):
    wks_result=wks.get_values('A','D')
    for x in  range(len(wks_result)):
        if date in wks_result[x][0]:
            today_data.append(wks_result[x])

def average():
    temp_data=[]
    humi_data=[]

    for x in range(len(today_data)):
        temp_data.append(float(today_data[x][3]))
    temp_avg = sum(temp_data)/len(temp_data)

    for x in range(len(today_data)):
        humi_data.append(float(today_data[x][4]))
    humi_avg = sum(humi_data)/len(humi_data)

    return {'Temperature': temp_avg, 'Humidity': humi_avg}
