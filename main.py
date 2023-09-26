import json
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.ebay.com/sch/i.html?'
params = {
    '_nkw' : 'samsung',
    '_trksid' : 'p2380057.m4084.l1312',
    '_sacat' : '0',
}
headers = {
    'user-agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
}

result = []
r = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')
content =soup.find_all('li', 's-item__pl-on-bottom')

try:
    os.mkdir('json_rsult')
except FileExistsError:
    pass



# 3. ekstraksi/mengambil data dari hasil parsing dengan perulangan
for item in content:
    title = item.find('div', 's-item__title').text
    try:
        price = item.find('span', 's-item__price').text
    except:
        continue
    try:
        location = item.find('span', 's-item__location').text
    except:
        continue
    try:
        ongkir = item.find('span', 's-item__shipping').text
    except:
        continue
    try:
        ratingseller = item.find('span', 's-item__etrs-text').text
    except:
        ratingseller = 'no rating'


    # 4. menampilkan data
    # Setelah mengambil data yang diperlukan dari elemen html, kode membuat sebuah dictionary (final_data) dengan
    # kunci yang sesuai (title, price, dll) dan mengisi nilai sesuai dengan data yang telah diambil.
    final_data = {
        'title': title,
        'price': price,
        'location': location,
        'ongkir': ongkir,
        'ratingseller': ratingseller,
    }
    # append (menampung data)
    result.append(final_data)

# 5. Menuliskan ke file json
#writing json
with open('json_rsult.json', 'w') as outfile:
    json.dump(result, outfile)
#read json
with open('json_rsult.json') as json_file:
    final_data = json.load(json_file)
    print(final_data)

# agar tampilan dibawah ini tidak menyamping tapi atas ke bawah
    for i in final_data:
        print(i)



# 6. writing data csv or excel
    df = pd.DataFrame(final_data)
    df.to_csv('result.csv', index=False)
    df.to_excel('result.xlsx', index=False)