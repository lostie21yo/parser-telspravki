import sys
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import os
import time

city = "Samara"
links = (
    "https://telspravki.info/rossiya/samarskaya-oblast/oblastnoj-tsyentr/samara?serchStreet=%21", # all
    "https://telspravki.info/rossiya/samarskaya-oblast/oblastnoj-tsyentr/samara?serchStreet=%CA", # К
    "https://telspravki.info/rossiya/samarskaya-oblast/oblastnoj-tsyentr/samara?serchStreet=%D1" # С
)
exception_symbol = ("К", "С") # исключения (обработать вручную)
alphabet = "0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper() # Общий алфавит
done = "0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper() # сохранение завершенных букв алфавита (за исключением отдельных букв в exception symbol)

file_dir = os.path.split(__file__)[0].replace('\\', '/')
try:
    df = pd.read_csv(f"{file_dir}/{city}.csv", delimiter='\t', encoding='utf-16') # old
except:
    df = pd.DataFrame(columns=('Address', 'Name', 'Number')) # new

def parse():
    main_r = requests.get(links[2])
    html = BS(main_r.content, 'html.parser')

    # Страница города с улицами
    count = 0
    for col in html.select(".col"):
        streets = col.select("a")
        for street in streets:
            # if street.text.startswith("Кол"):
            if street.text[0] == "С":
            # if street.text[0] in alphabet and street.text[0] not in done and street.text[0] not in exception_symbol: 
                print(f"=== {street.text} ===")
                street_r = requests.get(f"https:{street.get('href')}")
                html1 = BS(street_r.content, 'html.parser')

                # Страница улицы с домами
                for houselink in html1.select(".house"):
                    houses = houselink.select("a")
                    for house in houses:
                        # print("house: ", house.text)
                        house_r = requests.get(f"https:{house.get('href')}")
                        html2 = BS(house_r.content, 'html.parser')

                        # Страница дома с жителями
                        for row in html2.select(".res tr"):
                            cells = row.select("td")
                            number = cells[0].text
                            fio = cells[1].text
                            address = cells[2].text
                            df.loc[len(df.index)] = (address, fio, number)
                            count += 1
                            print(f"{count}.   {address}, {fio}, {number}")
                        
                        # обработка таблицы на несколько страниц
                        for pagelink in set(html2.select(".res a")):
                            try:
                                page_r = requests.get(f"https:{pagelink.get('href')}")
                                #print(pagelink.get('href'))
                                hrml3 = BS(page_r.content, 'html.parser')
                                for row in hrml3.select(".res tr"):
                                    cells = row.select("td")
                                    number = cells[0].text
                                    fio = cells[1].text
                                    address = cells[2].text
                                    df.loc[len(df.index)] = (address, fio, number)
                                    count += 1
                                    print(f"{count}.   {address}, {fio}, {number}")
                            except:
                                pass
                    
                df.to_csv(f'{file_dir}/{city}.csv', sep='\t', index= False, encoding="utf-16")  

start = time.time()            
parse()
finish = time.time() - start

print(f"Затраченное время {finish//60} мин {round(finish%60)} сек")


df = df.sort_values(by='Address', ascending=True)
for row in df.values:
    row[2] = " " + row[2]
df.to_csv(f'{file_dir}/{city}.csv', sep='\t', index= False, encoding="utf-16")
