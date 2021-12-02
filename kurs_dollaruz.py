import requests
from bs4 import BeautifulSoup


def get_malumot():
        url = 'https://dollaruz.pw/'
        site = requests.get(url)
        site = site.text
        soap = BeautifulSoup(site, 'lxml')
        banks = soap.find('div', class_="banks")
        table = banks.table
        result = '<b> Bugun kunning eng ishonchli dollar kurslari </b>'
        for i, tr in enumerate(table.find_all('tr')):
            strr = ''
            ban = '🏦 ⬆ ⬇ '.split(' ')

            for i, td in enumerate(tr):

                tex = td.text
                if i == 0:
                    strr = '<b>'+ban[0]+td.text+'</b> :'
                else:
                    strr = strr+'   ' + ban[i] +td.text
            print(strr[strr.find(ban[1])+1:strr.find(ban[2])-3])
            if strr[strr.find(ban[1])+1:strr.find(ban[2])-3].isdigit():
                result = result + '\n' +strr.removeprefix('\n')
        return result


if __name__ == '__main__':
    print(get_malumot())