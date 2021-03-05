from bs4 import BeautifulSoup as BS
from flask import Flask, render_template, request, url_for
import requests

class Item:
    def __init__(self, item_id):
        self.item_id=item_id
        self.reviews=[]
        self.getAllRevs(item_id)

    def getItemBlock(self,soup):
        rev_blocks = soup.find_all(class_="user-post user-post__card js_product-review")
        return rev_blocks

    def getItemRev(self,soup):
        user_blocks=self.getItemBlock(soup)
        for rev_block in user_blocks:
            # LOAD DATES FROM USER POSTS
            post_dates = rev_block.find(class_='user-post__published')

            user_dates = post_dates.find_all('time')
            number_of_dates = 0
            for i in user_dates:
                number_of_dates += 1

            # STORE USER INFO IN DICTIONARY
            info = {
                "desc": rev_block.find(class_='user-post__text').text,
                "stars": rev_block.find(class_='user-post__score-count').text,
                "author": rev_block.find(class_='user-post__author-name').text,
                "recommended": rev_block.find(class_='recommended').text if rev_block.find(
                    class_='recommended') is not None else '',
                "rev_date": user_dates[0]['datetime'],
                "buy_date": user_dates[1]['datetime'] if number_of_dates > 1 else ''
            }
            self.reviews.append(info)
    def getAllRevs(self,item_id):
        url = f'https://www.ceneo.pl/{item_id}#tab=reviews'
        page = requests.get(url)
        soup = BS(page.content, 'html.parser')
        self.getItemRev(soup)
        print(soup)
        if soup.find(class_='pagination'):
            pages_list = soup.find(class_='pagination')
            if pages_list.find(class_='pagination__item pagination__next'):
                next_page = True
                actual_page_num = 2
                while next_page:
                    npage_url = f'https://www.ceneo.pl/{item_id}/opinie-{actual_page_num}'
                    actual_page_num += 1
                    npage = requests.get(npage_url)
                    nsoup = BS(npage.content, 'html.parser')
                    self.getItemRev(nsoup)
                    npages_list = nsoup.find(class_='pagination')
                    if npages_list.find(class_='pagination__item pagination__next'):
                        next_page = True
                    else:
                        next_page = False
