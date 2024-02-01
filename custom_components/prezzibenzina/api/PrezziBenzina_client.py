import requests
from bs4 import BeautifulSoup
from PrezziBenzina import PrezziBenzina
BASE_URL = "https://www.prezzibenzina.it/distributori/{}"

class prezzibenzina_client:
    
    
    def id_exists(self, id) -> bool:
        if(not id):
            return False
        soup : BeautifulSoup = self._retrive_soup(id) 
        try:
            self._get_station_name(soup)
            return True
        except:
            return False
    
    def retrive_info(self, id) -> PrezziBenzina:
        soup : BeautifulSoup = self._retrive_soup(id) 
        station_name = self._get_station_name(soup)
        street = self._get_station_address(soup)
        values = self._get_values(soup)
        return PrezziBenzina(station_name, street, values)

    def _get_values(self, soup) -> list:
            gas_list = []
            table = soup.findAll('div', {"class": "st_reports_row"})
            for row in table[1:]: 
                gas = {
                    'date': row.find('div', {"class": "st_reports_data"}).text,
                    'fuel': row.find('div', {"class": "st_reports_fuel"}).text,
                    'service': row.find('div', {"class": "st_reports_service"}).text,
                    'price': self._convert_to_number(row.find('div', {"class": "st_reports_price"}).text)
                }
                gas_list.append(gas)
            return gas_list

    def _get_station_name(self, soup):
        return soup.find('div', {"class": "st_name"}).text

    def _get_station_address(self, soup):
        return soup.findAll('div', {"class": "st_address"})[-1].text + ", " + soup.find('div', {"class": "st_city"}).text

    def _retrive_soup(self,id) -> BeautifulSoup:
        r = requests.get(BASE_URL.format(id))
        return BeautifulSoup(r.text, 'html.parser')
    
    def _convert_to_number(self, string_value) -> BeautifulSoup:
       cleaned_price_text = ''.join(char if char.isdigit() or char == '.' or char == ',' else '' for char in string_value)
       return float(cleaned_price_text) 