from xml.etree import ElementTree

import requests

token_bot = 'your token id'
chat_id = 'your chat id'

def send_message_tg(text):
    """Sending a message to the Telegram Api. If the deadline has passed, then write in telegram"""
    url_request = "https://api.telegram.org/bot" + token_bot + \
              "/sendMessage" + "?chat_id=" + chat_id + \
              "&text=" + text
    requests.get(url_request)


def convert_usd_to_rub(cost_usd):
    """Method to getting the current USD/RUB exchange rate and converting"""
    
    #URL to parsing data 
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    
    # Parsing data
    res = requests.get(url).content
    exchange_rate = ElementTree.fromstring(res).findtext('.//Valute[@ID="R01235"]/Value')
    
    # Convert
    cost_in_rub = int(float(exchange_rate.replace(',', '.')) * float(cost_usd))

    return cost_in_rub