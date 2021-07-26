import requests
from bs4 import BeautifulSoup
import re
import csv

route = 'hospitals/'

service_url = "https://www.ccss.sa.cr/hospitales?v="
dataset = []

index = 1
while index <= 29:
    print("Working on: ",index)
    site = None
    retry = 0
    while site is None:
        retry += 1
        try:
            site = requests.get(service_url+str(index))
        except:
            print('Retry: ', retry)
            pass
    soup = BeautifulSoup (site.text, 'html.parser')

    tag = soup.find('div', {"class": 'page-article-content clearfix'})
    nombre = str(tag.find('h2').contents[0])
    


    ##coordinate scrapping
    """ coord_js= (soup.find_all('script')[-1]).string
    coord = coord_js.split('[')[1].strip()
    coord = coord.split(']')[0].strip()
    coord = coord.split(', ')
    """
    coord=(soup.find('small')).find('a')['href']
    coord = coord.split('/')[-2:]

    dataset.append([nombre, coord[1], coord[0]]) 

    index +=1
    


with open(route+"crss_hospitales.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Longitud', 'Latitud'])
    writer.writerows(dataset)
