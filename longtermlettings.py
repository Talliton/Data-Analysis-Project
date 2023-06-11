
import scrapy
import pandas as pd
import re
from scrapy.crawler import CrawlerProcess


class LongTermLettingsSpider(scrapy.Spider):
    name = "longtermlettings"
    start_urls = []
    for i in range(1, 6000):
        start_urls.append( f"https://www.longtermlettings.com/rent/pt/monthly/scr/cont6/page/{i}/")

    global results
    results = []

    def parse(self, response):
        # Используем CSS-селекторы для извлечения данных
        listings = response.css('div.searchrestable.boxshadowlight')

        for listing in listings:
            title = listing.css('span.txtsml::text').get()
            price = listing.css('div.pricefield::text').extract()[2]
            price = int(re.sub(r',', '', price))
            match_1 = re.findall(r'<b>(.+?) </b>', listing.css('div.searchbeds').get())
            if len(match_1) == 0:
                bedrooms, bathrooms = 0, 1
            elif len(match_1) == 1:
                bedrooms, bathrooms = 0, int(match_1[0])
            else:
                bedrooms, bathrooms = int(match_1[0]), int(match_1[-1])
            h = listing.css('div.search_bot_div').get()
            match_2 = re.search(r'longitude=([-\d\.]+)&amp;latitude=([-\d\.]+)', h)
            if match_2 == None:
                longitude = None
                latitude = None
            else:
                longitude = match_2.group(1)
                latitude = match_2.group(2)

            # Добавляем данные в список результатов
            results.append({
                'Title': title,
                'Price': price,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Longitude': longitude,
                'Latitude': latitude,
            })

        # Создаем DataFrame из списка результатов
        df = pd.DataFrame(results)

        # Выводим DataFrame в консоль
        print(df)
        df.to_csv('data/apartments.csv', index=False)


#%%
