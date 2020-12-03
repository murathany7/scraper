import csv
from bs4 import BeautifulSoup as soup
import requests
import gc

# num to redirect to links
num = 1
# These are to hold Questions and Responses, respectively
questions = []
responses = []
csvrow = ['Question', 'Response']
# create the file
with open('data.csv', mode='w', encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csvrow)
    writer.writeheader()


# method for questions with no pictures
def scrapNoPic(containerss, qstn):
    mesaj = containerss[0].findAll('p')
    if len(mesaj) > 0:
        newmsj = ''
        for msj in mesaj:
            newmsj += msj.text
        qstn[0] = str(newmsj)


# method to scrap for questions with pictures
def scrapwPic(container, qstn):
    mesaj = container[0].findAll('td')
    qstn[0] = str(mesaj[0].text.strip())


# while loop to get all the data from 1500 pages, each page has 10 links
while num < 1500:
    # Create the array to pass to the CSV file, qPlaceholder array to hold questions, answer to hold answers
    topass = []
    qPlaceholder = ['aa']
    answer = ''

    # create links to navigate
    myurl = 'https://forum.donanimhaber.com/forumid_2108/p_' + str(num) + '/tt.htm'
    try:
        r = requests.get(myurl)
    except:
        continue
    page_soup = soup(r.content, "html.parser")
    containers = page_soup.findAll("div", {"class": "kl-icerik-satir yenikonu"})
    # find the each link in each page
    for c in containers:
        # this is to see if the question has any answers
        answercount = float(c.findAll('div', {'class': 'kl-cevap'})[0].string)
        if answercount < 1:
            continue
        # find the url to scrap the data
        theurl = c.findAll("div", {'class': 'kl-konu'})[0].findAll('a')[0]
        completeurl = 'https://forum.donanimhaber.com' + theurl['href']
        try:
            re = requests.get(completeurl)
        except:
            print("URL alirken sorun cikti")
            continue
        container_soup = soup(re.content, 'html.parser')
        dataContainer = container_soup.findAll("span", {"class": "msg"})
        # check if the data has picture or not
        if dataContainer[0].findAll('p'):
            scrapNoPic(dataContainer, qPlaceholder)
        else:
            try:
                scrapwPic(dataContainer)
            except:
                continue
        # Below is to get a response
        # check if it is the best upvoted answer or any answer, give priority to the upvoted answer
        if container_soup.findAll("div", {"id": "bestMessagesContext"}):
            ansCount = container_soup.findAll("div", {"id": "bestMessagesContext"})
            answer = ansCount[0].findAll("div", {'class': 'icerik-content'})[0].text.strip()
        else:
            # check if there are responses. If not, print No answer and go to next one
            try:
                begenilmeyencevap = container_soup.findAll('span', {'class': 'msg'})
                answer = begenilmeyencevap[1].text.strip()
            except:
                print('No answer')
                continue
        questions.append(qPlaceholder[0])
        responses.append(answer)
        topass.append({'Question': qPlaceholder[0], 'Response': answer})
    # append question and answers as dictionary to the csv file at the end of the page
    with open('data.csv', mode='a', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csvrow)
        writer.writerows(topass)
    num += 3
    gc.collect()
