from bs4 import BeautifulSoup
import requests
import pandas as pd


def Scraping(de, a) :

    # get the url to scrap from
    urls = ["https://www.moroccoworldnews.com/covid-19/page/" + str(i) for i in range(de, a)]
    links = []
    rows = []
    # -------------------------- articles link------------------------

    for url in urls:
        # content of the web site
        html_cnt = requests.get(url).text
        # soup de scrap from the url
        soup = BeautifulSoup(html_cnt, 'lxml')
        # a for every article
        all_as = soup.select(".td-module-title a")
        for a in all_as:
            # link to every article
            links.append("https://www.moroccoworldnews.com/" + a['href'])

    # ------------------ getting the article content--------------
    for link in links:
        html_cnt = requests.get(link).text
        soup = BeautifulSoup(html_cnt, "lxml")
        row = {"link": link, "title": soup.select("header .entry-title")[0].string, "text": ''}
        for p in soup.select(".post-info-description p"):
            if p.string is None:
                continue
            row['text'] = row['text'] + p.string
        rows.append(row)
    
    return rows 
