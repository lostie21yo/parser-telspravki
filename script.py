import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import sys
import time

city = "г. Ставрополь, "
df = pd.read_csv("D:\\my\\Programming\\telspravki-parser\\Stavropol.csv", delimiter='\t', encoding='utf-16') # old
# df = pd.DataFrame(columns=('Address', 'Name', 'Number')) # new

links = (
    ("*", "https://telspravki.info/rossiya/stavropolskij-kraj/oblastnoj-tsyentr/stavropol?serchStreet=%21"), # All
    ("К", "https://telspravki.info/rossiya/stavropolskij-kraj/oblastnoj-tsyentr/stavropol?serchStreet=%CA"), # K
    ("П", "https://telspravki.info/rossiya/stavropolskij-kraj/oblastnoj-tsyentr/stavropol?serchStreet=%CF"), # П
    ("С", "https://telspravki.info/rossiya/stavropolskij-kraj/oblastnoj-tsyentr/stavropol?serchStreet=%D1"), # С
)

exception_symbol = ("К", "П", "С")
alphabet = "0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper()
done = "0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper()

def parse():
    main_r = requests.get(links[0][2])
    html = BS(main_r.content, 'html.parser')

    # Страница города с улицами
    limit = 0
    count = 0
    for col in html.select(".col"):
        streets = col.select("a")
        for street in streets:
            if street.text[0] == "П": #in alphabet[27:] and street.text[0] not in done and street.text[0] not in exception_symbol:
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
                    
                df.to_csv(r'D:/my/Programming/telspravki-parser/Stavropol.csv', sep='\t', index= False, encoding="utf-16")  

start = time.time()            
parse()
finish = time.time() - start

print(f"Затраченное время на парсинг {finish//60} мин {round(finish%60)} сек")

df = df.drop_duplicates()
df = df.sort_values(by='Address', ascending=True)
df.to_csv(r'D:/my/Programming/telspravki-parser/Stavropol.csv', sep='\t', index= False, encoding="utf-16")
