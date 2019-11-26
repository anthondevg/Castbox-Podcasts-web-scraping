import scrapy
import json
import re
from urllib.parse import urljoin

class CastBoxSpider(scrapy.Spider):
    name = 'castbox'
    
    # command to execute scrapy runspider castboxscraper.py -o podcasts.json
    start_urls = [ 'https://castbox.fm/categories?country=us' ]
    
    # get categories
    def parse(self, response):
        categories = response.xpath("//*[contains(@class, 'categoriesRow')]/a/@href").extract()
        for category in categories:
            
            url = urljoin(response.url, category)
            
            # get only the category_id from urls
            x = url.split('-')[-1]
            category_id = x.split('?')[0]
            
            # id extracted
            print("id => "+category_id) 
            
            limit = "220"
            final_url =  'https://everest.castbox.fm/data/top_channels/v2?category_id='+category_id+'&country=us&skip=0&limit='+limit+'&web=1'
            yield scrapy.Request(final_url, callback=self.parse_podcast)
      
    def parse_podcast(self, response):
        data = json.loads(response.body)
        
        for podcast in data.get('data',{}).get('list',[]):
            self.logger.info('Scraping data from castbox! ... ')
            yield {
                'category'        : data.get('data',{}).get('category',{}).get('name'),
                'title'           : podcast.get('title'),
                'author'          : podcast.get('author'),
                'uri'             : podcast.get('uri'),
                'suscribed'       : podcast.get('sub_count'),
                'played'          : podcast.get('play_count'),
                'episodes'        : podcast.get('episode_count'),
                'comments'        : podcast.get('comment_count'),
                'sub_categories'  : podcast.get('categories'),
                #'website'         : podcast.get('website'),
                #'keywords'        : podcast.get('keywords')
            }
            
        # categories 
    '''
        id => 10021 [Arts]
        id => 10028 [Business]
        id => 10035 [Comedy]
        id => 10039 [Education]
        id => 10044 [Fiction]
        id => 10048 [Leisure]
        id => 10057 [Government]
        id => 10058 [History]
        id => 10059 [Fitness]
        id => 10066 [Kids and Family]
        id => 10071 [Music]
        id => 10075 [News]
        id => 10083 [Religion & Spirituality]
        id => 10091 [Science]
        id => 10101 [Society & Culture ]
        id => 10107 [Sports]
        id => 10123 [Technology]
        id => 10124 [True Crime]
        id => 10125 [TV & Film]
        id => 105   [Audiobooks]
        https://castbox.fm/categories/Arts-10021?country=us
        https://castbox.fm/categories/Business-10028?country=us
        https://castbox.fm/categories/Comedy-10035?country=us
        https://castbox.fm/categories/Education-10039?country=us
        https://castbox.fm/categories/Fiction-10044?country=us
        https://castbox.fm/categories/Leisure-10048?country=us
        https://castbox.fm/categories/Government-10057?country=us
        https://castbox.fm/categories/History-10058?country=us
        https://castbox.fm/categories/Health-%26-Fitness-10059?country=us
        https://castbox.fm/categories/Kids-%26-Family-10066?country=us
        https://castbox.fm/categories/Music-10071?country=us
        https://castbox.fm/categories/News-10075?country=us
        https://castbox.fm/categories/Religion-%26-Spirituality-10083?country=us
        https://castbox.fm/categories/Science-10091?country=us
        https://castbox.fm/categories/Society-%26-Culture-10101?country=us 
        https://castbox.fm/categories/Sports-10107?country=us
        https://castbox.fm/categories/Technology-10123?country=us
        https://castbox.fm/categories/True-Crime-10124?country=us
        https://castbox.fm/categories/TV-%26-Film-10125?country=us
        https://castbox.fm/categories/Audiobooks-105?country=us
        
    '''
    ''' 
        Script developed by Robwert Mota 11/2019  for Jack Rhysider to get data from castbox's podcasts
        ---
        @robwert1997@gmail.com
        telegram : @arentus
        website  : http://arentus.github.io/ 
        
    ''' 