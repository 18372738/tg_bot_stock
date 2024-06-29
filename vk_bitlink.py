import os
import requests
from dotenv import load_dotenv


load_dotenv()

VK_ACCESS_TOKEN = os.getenv('VK_TOKEN')
VK_API_VERSION = '5.131'

def shorten_link_vkontakte(original_url):
    url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "url": original_url,
        "access_token": VK_ACCESS_TOKEN,
        "v": VK_API_VERSION
    }

    response = requests.get(url, params=params)
    response_data = response.json()
    if 'response' in response_data:
        return response_data['response']['short_url']
    elif 'error' in response_data:
        raise Exception(f"Ошибка сокращения ссылки: {response_data['error']['error_msg']}")
    else:
        raise Exception(f"Неизвестная ошибка: {response_data}")

def get_clicks_vkontakte(short_url):
    url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "key": short_url.split('/')[-1],
        "access_token": VK_ACCESS_TOKEN,
        "v": VK_API_VERSION
    }

    response = requests.get(url, params=params)
    response_data = response.json()
    if 'response' in response_data:
        return response_data['response']['stats']
    elif 'error' in response_data:
        raise Exception(f"Ошибка получения статистики: {response_data['error']['error_msg']}")
    else:
        raise Exception(f"Неизвестная ошибка: {response_data}")
