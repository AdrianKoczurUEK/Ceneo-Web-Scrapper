from flask import Flask, render_template, request
from bs4 import BeautifulSoup as BS
import requests

app = Flask(__name__)


@app.route('/')
def homePage():
    return render_template('index.html')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    item_id = request.form['item_id']
    page_url = f'https://www.ceneo.pl/{item_id}#tab=reviews'
    page = requests.get(page_url)
    soup = BS(page.content, 'html.parser')

    # LOAD USER INFO CONTAINER
    rev_blocks = soup.find_all(class_="user-post user-post__card js_product-review")
    user_data = []
    for rev_block in rev_blocks:
        # LOAD DATES FROM USER POSTS
        post_dates = rev_block.find(class_='user-post__published')
        user_dates = post_dates.find_all('time')
        x=0
        for i in user_dates:
            x+=1

        # STORE USER INFO IN DICTIONARY
        info = {
            "desc": rev_block.find(class_='user-post__text').text,
            "stars": rev_block.find(class_='user-post__score-count').text,
            "author": rev_block.find(class_='user-post__author-name').text,
            "recommended": rev_block.find(class_='recommended').text if rev_block.find(
                class_='recommended') is not None else '',
            "rev_date": user_dates[0]['datetime'],
            "buy_date": user_dates[1]['datetime'] if x>1 else ''
        }
        user_data.append(info)

    rev_pros = soup.find_all(class_='review-feature__col')
    return render_template('data.html', user_data=user_data)


if __name__ == '__main__':
    app.run(debug=True)
