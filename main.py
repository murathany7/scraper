import requests
from bs4 import BeautifulSoup
import pandas as pd

num = 1
my_data=[]
df=pd.DataFrame(data=my_data,columns=['Headline'])
df.to_csv('scraped.csv', index=False, mode="a")
while num<250:
    my_data = []
    URL = "https://cryptonews.net/?page=" + str(num)
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    results = soup.find_all("div", class_="desc col-xs")
    for a in results:
        print(a.a.text)
        my_data.append(a.a.text)

    df=pd.DataFrame(data=my_data,columns=['Headline'])
    df.to_csv('scraped.csv', index=False, mode="a", header=False)

    num = num + 1
    page.close()
    print(num)






# print(soup.prettify())