import requests
from bs4 import BeautifulSoup
import concurrent.futures
from scraper_api import ScraperAPIClient
import csv
import urllib.parse
import json
import pandas as pd
restaurant_name = "15" 
headers = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41',
    'Accept-Language': 'zh-TW'
}
client = ScraperAPIClient("YOUR_APIKEY")
NUM_RETRIES = 3
NUM_THREADS = 3
#建立author, grade, comment來存放資料
author = []
grade = []
comment = []
## Example list of urls to scrape
list_of_urls = []
for i in range(1, 100):
    
    url = "https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=zh-TW&gl=tw&pb=!1m2!1y3765758267439148725!2y7426342362123979922!2m2!1i"+str(i*10)+"!2i10!3e4!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1seBGfYobnNdSY-Aa6hrToBg!7e81"
    list_of_urls.append(url)



def scrape_url(url):
    # send request to scraperapi, and automatically retry failed requests
    for _ in range(NUM_RETRIES):
        response = client.get(url, retry=NUM_RETRIES,headers=headers)
        if response.status_code in [200, 404]:
            ## escape for loop if the API returns a successful response
            break

    ## parse data if 200 status code (successful response)
    if response.status_code == 200:
        ## Example: parse data with beautifulsoup
        text = response.text
        
        pretext = ')]}\''
        text = text.replace(pretext,'')
        # 把字串讀取成json
        soup = json.loads(text)
        # 取出包含留言的List 。
        conlist = soup[2]

        # 逐筆抓出
        for j in conlist:
            author.append(str(j[0][1]))
            comment.append(str(j[3]))
            grade.append(str(j[4]))

with concurrent.futures.ThreadPoolExecutor(
        max_workers=NUM_THREADS) as executor:
    executor.map(scrape_url, list_of_urls)

print(f"已抓取完畢..")
#整體成pd
google_comment_df = pd.DataFrame({
    "author":author,
    "grade":grade,
    "comment":comment,    
    })

google_comment_df.to_excel("excel/"+restaurant_name+".xlsx", index=False)