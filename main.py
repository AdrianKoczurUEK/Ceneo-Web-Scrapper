from flask import Flask, render_template
from bs4 import BeautifulSoup as BS
import requests
app = Flask(__name__)
page_url = 'https://www.ceneo.pl/90136842#tab=reviews'
page = requests.get(page_url)
soup = BS(page.content, 'html.parser')
rev_text=soup.find_all(class_='user-post__text')
rev_stars=soup.find_all(class_='user-post__score-count')
rev_pros=soup.find_all(class_='review-feature__col')

@app.route('/')
def hello_world():
    return render_template('index.html',texts=user)

if __name__=='__main__':
    app.run(debug=True)