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
   
    # LOAD REVIEW COMMENTS
    rev_blocks = soup.find_all(class_="user-post user-post__card js_product-review")
    rev_texts_content=[]
    for rev_block in rev_blocks:
        rev_text = rev_block.find(class_='user-post__text')  # you get list
        rev_texts_content.append(rev_text.text)



    rev_stars = soup.find_all(class_='user-post__score-count')
    rev_pros = soup.find_all(class_='review-feature__col')
    return render_template('data.html',rev_text=rev_texts_content)

if __name__=='__main__':
    app.run(debug=True)