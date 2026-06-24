import requests
from bs4 import BeautifulSoup
def get_price(url):
    try:
        response=requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup=BeautifulSoup(response.text, 'html.parser')
        price_element=soup.find('meta', {'property': 'product:price:amount'})
        if price_element:
            return price_element["content"]
        return None
    except Exception as e:
        print("Ошибка:", e)
        return None
print(get_price("https://kaspi.kz/shop/p/apple-iphone-17-pro-256gb-nanosim-esim-oranzhevyi-145467625/?c=750000000"))

