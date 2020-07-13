#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 08:42:34 2020

@author: mcgaritym
"""

# import packages
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import date, datetime
import re
import time

# set driver options and request options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--incognito')
driver = webdriver.Chrome(ChromeDriverManager().install())
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.39 Safari/537.36', 
           "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

# create function for given url input
def fin_news_scraper(*urls):

    # create empty list            
    list_news = []
    
    #for loop for variable # of url inputs to function
    for url in urls:
        
        # get link, use bs4 to parse
        #driver.manage().timeouts().implicitlyWait(TimeOut, TimeUnit.SECONDS)        
        time_0 = time.time()
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 1000)")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 3000)")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 7000)")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 250000)")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 500000)")
        response_delay = time.time() - time_0
        time.sleep(10*response_delay)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        date_today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(response_delay, response_delay*10)
        # if statement based on url string
        
        if 'forbes' in url:
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('a', class_ = 'happening__title'):
            #     # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'forbes', 'date': date_today})) 
            for t in soup.find_all('a', class_ = re.compile('data-viz__title')):
                list_news.append(dict({'headline': t.text, 'org':'forbes', 'date': date_today}))                  
            for t in soup.find_all('a', class_ = re.compile('h1--dense')):
                list_news.append(dict({'headline': t.text, 'org':'forbes', 'date': date_today}))               
            for t in soup.find_all('h3', class_ = 'h3--dense'):
                list_news.append(dict({'headline': t.text, 'org':'forbes', 'date': date_today}))                          
            for t in soup.find_all('a', class_ = 'headlink h4--dense'):
                 list_news.append(dict({'headline': t.span.contents[0], 'org':'forbes', 'date': date_today}))             
            for t in soup.find_all('a', attrs = {'data-ga-track': re.compile('Channel - Block')}):
                 list_news.append(dict({'headline': t.text, 'org':'forbes', 'date': date_today})) 
            for t in soup.find_all('h2', class_ = re.compile('h4--dense')):
                list_news.append(dict({'headline': t.text, 'org':'forbes', 'date': date_today}))                

        if 'marketwatch' in url:
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('a', class_ = 'latestNews__headline'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.span.text, 'org':'marketwatch', 'date': date_today}))
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('h3', class_ = 'article__headline'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'marketwatch', 'date': date_today}))           
            for t in soup.find_all('li', class_ = 'bullet__item'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'marketwatch', 'date': date_today}))             
            for t in soup.find_all('h3', class_ = 'article__headline'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'marketwatch', 'date': date_today}))  

        if 'wsj' in url:
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('h3', class_ = re.compile('WSJTheme--headline')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'wsj', 'date': date_today}))
            for t in soup.find_all('h3', class_ = re.compile('style--headline')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'wsj', 'date': date_today}))
            for t in soup.find_all('h3', class_ = re.compile('WSJTheme--title')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'wsj', 'date': date_today}))
            for t in soup.find_all('div', class_ = re.compile('style--text')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.h3.span.contents[0], 'org':'wsj', 'date': date_today}))

        if 'bloomberg' in url:
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('a', class_ = re.compile('single-story-module')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'bloomberg', 'date': date_today}))
            for t in soup.find_all('a', class_ = re.compile('story-package-module')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'bloomberg', 'date': date_today}))
            for t in soup.find_all('section', class_ = re.compile('single-story-module')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'bloomberg', 'date': date_today}))

            for t in soup.find_all('h3', class_ = re.compile('story-package-module')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'bloomberg', 'date': date_today}))

        if 'reuters' in url:
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('h3', class_ = 'story-title'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'cnn', 'date': date_today}))
            for t in soup.find_all('h3', class_ = 'video-heading'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'cnn', 'date': date_today}))
        
        # NOTE: investopedia has lots of dated/old articles, not up to date       
        if 'investopedia' in url:
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('span', class_ = 'card__title'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'cnn', 'date': date_today}))
           
        if 'cnn' in url:
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('h2', class_ = 'banner-text'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'cnnbusiness', 'date': date_today}))            
            for t in soup.find_all('span', class_ = 'cd__headline-text'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'cnnbusiness', 'date': date_today}))
            
        if 'cnbc' in url:
            # for loop iterates over matching HTML (site specific) and extracts text
            for t in soup.find_all('h2', re.compile('FeaturedCard')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'cnbc', 'date': date_today}))                                   
            for t in soup.find_all('div', class_ = 'LatestNews-headline'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'cnbc', 'date': date_today}))                  
            for t in soup.find_all('li', id = re.compile('FeaturedCard')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'cnbc', 'date': date_today}))             
            for t in soup.find_all('div', class_ = 'SecondaryCard-headline'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'cnbc', 'date': date_today}))             
            for t in soup.find_all('div', class_ = re.compile('RiverHeadline')):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.a.text, 'org':'cnbc', 'date': date_today}))             
            for t in soup.find_all('a', class_ = 'Card-title'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.div.text, 'org':'cnbc', 'date': date_today}))             
            for t in soup.find_all('a', class_ = 'TrendingNowItem-title'):
                # append dictionary with headline, organization, and current date to empty list
                list_news.append(dict({'headline': t.text, 'org':'cnbc', 'date': date_today}))             
                                                                                                  
        if 'ibtimes' in url:
            for t in soup.find_all(name='h3'):
                list_news.append(dict({'headline': t.a.text, 'org':'ibtimes', 'date': date_today}))                             
            for t in soup.find_all(name='li'):
                list_news.append(dict({'headline': t.a.text, 'org':'ibtimes', 'date': date_today}))                             
            for t in soup.find_all(name='div', class_ = 'title'):
                list_news.append(dict({'headline': t.a.text, 'org':'ibtimes', 'date': date_today}))                             
            for t in soup.find_all(name='div', class_ = 'item-link'):
                list_news.append(dict({'headline': t.a.text, 'org':'ibtimes', 'date': date_today}))                             
            for t in soup.find_all(name='h4'):
                list_news.append(dict({'headline': t.a.text, 'org':'ibtimes', 'date': date_today}))                             
                             
        if 'seekingalpha' in url:
            for t in soup.find_all('a', class_ = '_2when'):
                list_news.append(dict({'headline': t.text, 'org':'seekingalpha', 'date': date_today})) 
            for t in soup.find_all('h3', class_ = re.compile('_1W')):
                list_news.append(dict({'headline': t.text, 'org':'seekingalpha', 'date': date_today})) 
      
        if 'fortune' in url:
            for t in soup.find_all('a', class_ = re.compile('featureModule__title')):
                list_news.append(dict({'headline': t.text, 'org':'fortune', 'date': date_today})) 
            for t in soup.find_all('div', class_ = re.compile('featureModule__excerpt')):
                list_news.append(dict({'headline': t.text, 'org':'fortune', 'date': date_today})) 
            for t in soup.find_all('a', class_ = re.compile('contentItem__')):
                list_news.append(dict({'headline': t.text, 'org':'fortune', 'date': date_today})) 
            for t in soup.find_all('a', class_ = re.compile('featureThreeGrid__titleLink')):
                list_news.append(dict({'headline': t.text, 'org':'fortune', 'date': date_today})) 
            for t in soup.find_all('a', class_ = re.compile('grid__titleLink')):
                list_news.append(dict({'headline': t.text, 'org':'fortune', 'date': date_today}))                                                     
            for t in soup.find_all('a', class_ = re.compile('rundownFeature__title')):
                list_news.append(dict({'headline': t.text, 'org':'fortune', 'date': date_today}))                                                     
            for t in soup.find_all('a', class_ = re.compile('rundownItem__title')):
                list_news.append(dict({'headline': t.text, 'org':'fortune', 'date': date_today}))                                                     
                
        if 'economist' in url:
            for t in soup.find_all('h1', class_ = 'weekly-edition-header__headline'):
                list_news.append(dict({'headline': t.text, 'org':'economist', 'date': date_today}))             
            for t in soup.find_all('span', class_ = re.compile('teaser__subheadline')):
                list_news.append(dict({'headline': t.text, 'org':'economist', 'date': date_today}))
            for t in soup.find_all('span', class_ = re.compile('teaser__headline')):
                list_news.append(dict({'headline': t.text, 'org':'economist', 'date': date_today}))                  
 
        if 'morningstar' in url:
            for t in soup.find_all('span', class_ = re.compile('mds-list-group__item')):
                list_news.append(dict({'headline': t.text, 'org':'morningstar', 'date': date_today}))           
            for t in soup.find_all('a', class_ = re.compile('mdc-link mdc-tag')):
                list_news.append(dict({'headline': t.text, 'org':'morningstar', 'date': date_today}))           
            for t in soup.find_all('span', attrs={"itemprop": "name"}):
                list_news.append(dict({'headline': t.text, 'org':'morningstar', 'date': date_today}))           
            for t in soup.find_all('a', class_ = re.compile('mdc-link mds-link')):
                list_news.append(dict({'headline': t.text, 'org':'morningstar', 'date': date_today}))           
            for t in soup.find_all('h2', class_ = re.compile('mdc-heading mdc-video')):
                list_news.append(dict({'headline': t.text, 'org':'morningstar', 'date': date_today}))           

        if 'financialtimes' in url:
            for t in soup.find_all('a', class_ = re.compile('js-teaser-heading')):
                list_news.append(dict({'headline': t.text, 'org':'financialtimes', 'date': date_today}))                                              
            for t in soup.find_all('a', class_ = re.compile('js-teaser-standfirst')):
                list_news.append(dict({'headline': t.text, 'org':'financialtimes', 'date': date_today}))                                              
            for t in soup.find_all('li', class_ = re.compile('o-teaser__related')):
                list_news.append(dict({'headline': t.a.text, 'org':'financialtimes', 'date': date_today}))                                              

        if 'thestreet' in url:
            for t in soup.find_all('h2', class_ = re.compile('header-text')):
                list_news.append(dict({'headline': t.text, 'org':'foxnews', 'date': date_today}))         
          
                                                
       
        
        
        if 'fox' in url:
            for t in soup.find_all('h2', class_ = 'title'):
                list_news.append(dict({'headline': t.text, 'org':'foxnews', 'date': date_today}))         
                
        if 'dailymail' in url:
            for t in soup.find_all(name='a', attrs={"itemprop": "url"}):
                list_news.append(dict({'headline': t.text, 'org':'dailymail', 'date': date_today}))   
    
        if 'huff' in url:
            for t in soup.find_all('h3', class_="card__headline__text"):
                list_news.append(dict({'headline': t.text, 'org':'huffingtonpost', 'date': date_today}))
        
        if 'nbc' in url:
            for t in soup.find_all(name='span', class_=re.compile("headline")):
                list_news.append(dict({'headline': t.text, 'org':'nbcnews', 'date': date_today}))     
            for t in soup.find_all(name='h2', class_=re.compile("headline")):
                list_news.append(dict({'headline': t.text, 'org':'nbcnews', 'date': date_today})) 
            for t in soup.find_all(name='h3', class_=re.compile("headline")):
                list_news.append(dict({'headline': t.text, 'org':'nbcnews', 'date': date_today})) 
                    
                
        if 'nytimes' in url:
            for t in soup.find_all(name='span', class_=re.compile('css-')):
                list_news.append(dict({'headline': t.text, 'org':'nytimes', 'date': date_today})) 
            for t in soup.find_all(name='h2', class_=re.compile('css-')):
                list_news.append(dict({'headline': t.text, 'org':'nytimes', 'date': date_today}))                
    
        if 'washingtonpost' in url:
            for t in soup.find_all(name='a', attrs={"data-pb-field": "headlines.basic"}):
                list_news.append(dict({'headline': t.text, 'org':'washingtonpost', 'date': date_today})) 
    
        if 'guardian' in url:
            for t in soup.find_all(name='a', attrs={"data-link-name": "article"}):
                list_news.append(dict({'headline': t.text, 'org':'theguardian', 'date': date_today}))  
                
        if 'google' in url:
            for t in soup.find_all(name='a', href = re.compile("^./articles")):
                list_news.append(dict({'headline': t.text, 'org':'google', 'date': date_today})) 
               
                
        if 'finance.yahoo' in url:
            for t in soup.find_all(name='h2', class_=re.compile('Fz(22px)--')):
                list_news.append(dict({'headline': t.text, 'org':'yahoofinance', 'date': date_today})) 
            for t in soup.find_all(name='h3', class_=re.compile('Fz(14px)--')):
                list_news.append(dict({'headline': t.text, 'org':'yahoofinance', 'date': date_today})) 
            for t in soup.find_all(name='a', class_=re.compile('Fw(b)')):
                list_news.append(dict({'headline': t.text, 'org':'yahoofinance', 'date': date_today})) 
               
        # else:
        #     print('Error: URL not found')
            
        #create pandas dataframe based on list with extracted info, with headlne, organization, and date columns
        df = pd.DataFrame(list_news, columns=['headline', 'org', 'date'])
        print(df) 
        
    # print(df.groupby('org')['headline'].count())
    # df.to_csv('fin_news_headlines__' + str(datetime.now().strftime("%Y-%m-%d__%H-%M-%S")) + '.csv', index=False)

fin_news_scraper(#'https://www.forbes.com/',
            #  'https://www.marketwatch.com/',
            #  'https://www.wsj.com/',
            #  'https://www.bloomberg.com/',
            # 'https://www.reuters.com/finance',
            # 'https://www.reuters.com/news/archive/businessnews?page=1',
            # 'https://www.reuters.com/news/archive/businessnews?page=2',
            # 'https://www.reuters.com/news/archive/businessnews?page=3',
            # 'https://www.reuters.com/news/archive/businessnews?page=4',
            # 'https://www.reuters.com/news/archive/businessnews?page=5',  
            #  'https://www.investopedia.com/company-news-4427705',
            #  'https://www.cnn.com/business/',
            #  'https://www.cnbc.com/',
            #   'https://www.ibtimes.com/',
            #  'https://seekingalpha.com/',
            #  'https://fortune.com/',
            #  'https://www.economist.com/weeklyedition',
            #  'https://www.morningstar.com/',
            #  'http://www.financialtimes.com/',
              'https://www.thestreet.com/')
            #  'https://www.msn.com/en-us/money',
            #  'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen',
            #  'https://www.fool.com/investing-news/',
            #  'https://www.foxbusiness.com',
            #  'https://finance.yahoo.com/')
    