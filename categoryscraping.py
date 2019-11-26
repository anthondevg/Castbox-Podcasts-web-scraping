import scrapy
import json
import re
from urllib.parse import urljoin

class CategoryCast(scrapy.Spider):
    name = 'categorycastbox'
    # get podcast from 0 to 220 in the 'Art' category. (id=10021)
    
    # command to execute scrapy crawl categorycastbox -a category=[id] -a limit=[0,220] default: 220 
    
    def __init__(self, category=None, limit="220", *args, **kwargs):
        super(CategoryCast, self).__init__(*args, **kwargs)
        
        if(category):
            print("limit = "+limit+" Category = "+category)
            format_base_url =  'https://everest.castbox.fm/data/top_channels/v2?category_id=%s&country=us&skip=0&limit=%s&web=1'
            self.start_urls = [ format_base_url % (category, limit) ]    
        else:
            print("\nERROR: Missing category argument. Please, Try the next command: \n\n scrapy runspider categoryscraping.py -a category=[id] -a limit=[0,220]")
            print(
            """
                Available categories
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
            """)
            pass        
                      
    def parse(self, response):
        data = json.loads(response.body)
        
        for podcast in data.get('data',{}).get('list',[]):
            self.logger.info('Scraping data from castbox! ... ')
            yield {
                'category' : data.get('data',{}).get('category',{}).get('name'),
                'title'     : podcast.get('title'),
                'author'    : podcast.get('author'),
                'uri'       : podcast.get('uri'),
                'suscribed' : podcast.get('sub_count'),
                'played'    : podcast.get('play_count'),
                'episodes'  : podcast.get('episode_count'),
                'comments'  : podcast.get('comment_count'),
                'sub_categories'  : podcast.get('categories')   
            }
     