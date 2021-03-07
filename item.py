from bs4 import BeautifulSoup as BS
from flask import Flask, render_template, request, url_for
from review import Review
from os.path  import basename
from urllib.request import urlopen
import requests


class Item:
    def __init__(self, item_id):
        self.item_url = f'https://www.ceneo.pl/{item_id}#tab=reviews'
        self.page = requests.get(self.item_url)
        self.soup = BS(self.page.content, 'html.parser')
        self.item_id = item_id
        self.item_name = self.getItemName()
        self.reviews=[]
        self.generateRevs(item_id)
        self.img=self.getImg()

    def getImg(self):
        try:
            link=self.soup.find("a", attrs={"class":'js_gallery-anchor js_image-preview'})
            linn=link.find("img")
            lnk = linn["src"]
            with open(f"images/{self.item_id}.jpg", "wb") as f:
                f.write(urlopen(f'http://{lnk[2:]}').read())
            return f"images/{self.item_id}.jpg"
        except:
            return ''

    def getItemName(self):
        page = requests.get(self.item_url)
        soup = BS(page.content, 'html.parser')
        return soup.find(class_='js_searchInGoogleTooltip breadcrumbs__item').text

    def createRevObj(self, soup):
        rev_blocks = soup.find_all(class_="user-post user-post__card js_product-review")
        for block in rev_blocks:
            self.reviews.append(Review(block))

    def generateRevs(self, item_id):
        url = f'https://www.ceneo.pl/{item_id}#tab=reviews'
        page = requests.get(url)
        soup = BS(page.content, 'html.parser')
        self.createRevObj(soup)
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
                    self.createRevObj(nsoup)
                    npages_list = nsoup.find(class_='pagination')
                    if npages_list.find(class_='pagination__item pagination__next'):
                        next_page = True
                    else:
                        next_page = False
