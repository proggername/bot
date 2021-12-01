import requests
from bs4 import BeautifulSoup


def get_malumot():
        url = 'https://dollaruz.pw/'
        site = requests.get(url)
        site = site.text
        soap = BeautifulSoup(site, 'lxml')
        banks = soap.find('div', class_="banks")
        table = banks.table
        result = '<b> Bugun kunning eng ishonchli dollar kurslari</b>\n'
        for i, tr in enumerate(table.find_all('tr')):
            strr = ''
            ban = '🏦⬆️⬇️'
            for td in tr:
                tex = td.text
                if str(tex).find('-') != -1:
                    continue
                strr = strr + td.text + ' || '
            result = result +strr[:-4]+'\n'
        return result


if __name__ == '__main__':
    get_malumot()