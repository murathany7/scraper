import requests
from bs4 import BeautifulSoup

URL = "https://cryptonews.net/?q=doge"
page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")
results = soup.find_all("div", class_="desc col-xs")
for a in results:
    print(a.a.text)
page.close()



