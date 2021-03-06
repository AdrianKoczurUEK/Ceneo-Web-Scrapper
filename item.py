from bs4 import BeautifulSoup as BS
from flask import Flask, render_template, request, url_for
import requests

class Item:
    id=1
    def __init__(self, item_id):
        self.item_id=item_id
        self.reviews=[]
        self.getAllRevs(item_id)

    def getItemBlock(self,soup):
        rev_blocks = soup.find_all(class_="user-post user-post__card js_product-review")
        return rev_blocks
    def getRevId(self):
        return self.id

    def getItemRev(self,soup):
        user_blocks=self.getItemBlock(soup)
        for rev_block in user_blocks:
            # dates
            post_dates = rev_block.find(class_='user-post__published')
            user_dates = post_dates.find_all('time')
            number_of_dates = 0
            for i in user_dates:
                number_of_dates += 1

            #recomendations
            recomendation=''
            if rev_block.find(class_='recommended'):
                recomendation=rev_block.find(class_='recommended').text
            elif rev_block.find(class_='not-recommended'):
                recomendation=rev_block.find(class_='not-recommended').text
            #pros and cons
            pros_list = []
            cons_list = []
            if rev_block.find(class_='review-feature'):
                col=rev_block.find_all(class_='review-feature__col')
                if len(col)>1:
                    pros=col[0].find_all(class_='review-feature__item')
                    for pro in pros:
                        pros_list.append(pro.text)
                    cons = col[1].find_all(class_='review-feature__item')
                    for con in cons:
                        cons_list.append(con.text)
                elif len(col)==1:
                    pros = col[0].find_all(class_='review-feature__item')
                    for pro in pros:
                        pros_list.append(pro.text)


            # STORE USER INFO IN DICTIONARY
            info = {
                "id": Item.getRevId(self),
                "desc": rev_block.find(class_='user-post__text').text,
                "stars": rev_block.find(class_='user-post__score-count').text,
                "author": rev_block.find(class_='user-post__author-name').text,
                "recommended": recomendation,
                "rev_date": user_dates[0]['datetime'],
                "buy_date": user_dates[1]['datetime'] if number_of_dates > 1 else '',
                "pros":pros_list,
                "cons":cons_list
            }
            self.id+=1
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
