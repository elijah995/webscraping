from selenium import webdriver
from bs4 import BeautifulSoup
import os

chromedriver = 'chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=3')
browser = webdriver.Chrome(executable_path=chromedriver, options=options)

browser.get('https://quotes.ino.com/charting/?s=FOREX_USDRUB')
requiredHtml = browser.page_source

soup = BeautifulSoup(requiredHtml, 'html5lib')

table = soup.findChildren('table')
my_table = table[0]
rows = table[0].findChildren(['th', 'tr'])
values = []
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.text
        values.append(value)
        
update = values[-1][:10] + ';' + values[0] + '\n'

mod_file = 'usd_quotes.csv'

with open(mod_file, 'r', encoding='utf8') as fin:
    data = []
    for line in fin.readlines():
        data.append(line)

if data[1].split(';')[0] != values[-1][:10]:
    with open(mod_file, 'w', encoding='utf8') as fout:
        fout.write(data[0])
        fout.write(update)
        for line in data[1:]:
            fout.write(line)

    print(mod_file + ' successfully updated')
    print('date:\t' + values[-1][:10])
    print('rate:\t' + values[0])

else:
    print(mod_file + ' has already been updated today')
    print('date:\t' + data[1].split(';')[0])
    print('rate:\t' + data[1].split(';')[1])

browser.quit()
