import json
from scraper_api import ScraperAPIClient
from outscraper import ApiClient
import pandas as pd
headers = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41',
    'Accept-Language':'zh-TW'
}
client = ScraperAPIClient("YOUR_APIKEY")
restaurant_name = "2" 

#建立author, grade, comment來存放資料
author =[]
grade = []
comment = []


for i in range(1,600):  #由上圖，判斷range上限，控制在小於等於 <= [(最大評論數/10)-1]
    
    # 發送get請求 
    url = "https://www.google.com.tw/maps/preview/review/listentitiesreviews?gl=tw&pb=!1m2!1y3776617339609336297!2y16182214227594615972!2m2!1i"+str(i*8)+"!2i8!4m1!3b1!5m7!4m1!2i23934!7e140!9slFaaYv6UHoTFhwP-5JGgAQ%3A798357979481!17slFaaYv6UHoTFhwP-5JGgAQ%3A798357979482!24m1!2e1"
    

    text = client.get(url, retry=3,headers=headers).text
    # 取代掉特殊字元，這個字元是為了資訊安全而設定的喔。
    pretext = ')]}\''
    
    text = text.replace(pretext,'')
    # 把字串讀取成json
    print(text)
    soup = json.loads(text)

    # 取出包含留言的List 。
    conlist = soup[2]

    # 逐筆抓出
    for j in conlist:
        author.append(str(j[0][1]))
        comment.append(str(j[3]))
        grade.append(str(j[4]))

    
                                            
print(f"已抓取完畢..")
#整體成pd
google_comment_df = pd.DataFrame({
    "author":author,
    "grade":grade,
    "comment":comment,    
    })

google_comment_df.to_csv(restaurant_name+".csv", index=False)