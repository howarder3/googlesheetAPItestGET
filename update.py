# update.py
import time
import gspread
import re
import datetime

from urllib.request import urlopen

from bs4 import BeautifulSoup

from oauth2client.service_account import ServiceAccountCredentials

def get_cheapest(url, text):
    with urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'lxml')

    cheapest_price = cheapest_item = None

    re_price = re.compile(r'\$(\d+)')
    root = soup.find('td', text=re.compile(text)).parent

    for option in root.find_all('option', text=re_price):
        item = option.text.strip()
        price = int(re_price.search(item).group(1))
        if cheapest_price is None or price < cheapest_price:
            cheapest_price = price
            cheapest_item = item

    return (cheapest_item, cheapest_price)

coolpc_url = 'http://www.coolpc.com.tw/evaluate.php'
ram_text = 'RAM'

# (cheapest_item, cheapest_price) = get_cheapest(coolpc_url, ram_text)

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

auth_json_path = "./auth.json"
gss_scopes = ['https://spreadsheets.google.com/feeds']

gss_client = auth_gss_client(auth_json_path, gss_scopes)

def update_sheet(gss_client, key, today,year,month,day, hr, minute,second):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([today, year,month,day,hr, minute, second], 2)

spreadsheet_key = "19nQvlQIGRIoGELFxGfHWazG45DM7D2GccZg8wlD85_g"	
# spreadsheet_key_path = 'spreadsheet_key'
now = datetime.datetime.now()

# if cheapest_price is not None:
today = time.strftime("%c")
# with open(spreadsheet_key_path) as f:
#    spreadsheet_key = f.read().strip()
update_sheet(gss_client, spreadsheet_key, today, now.year,now.month,now.day,now.hour,now.minute,now.second)

# update.py




