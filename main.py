from flask import Flask, render_template, request, url_for
from bs4 import BeautifulSoup as BS
from item import Item
import requests

app = Flask(__name__)
@app.route('/list')
def item_list():
    return render_template('item_list.html',page='list')

@app.route('/')
def homePage():
    return render_template('index.html',page='home')

@app.route('/extract')
def extract():
    return render_template('extract.html',page='extract')


@app.route('/extract_data', methods=['POST'])
def extract_data():
        item_id = request.form['item_id']
        item=Item(item_id)
        return render_template('extract.html', user_data=item.reviews, page='extract')



if __name__ == '__main__':
    app.run(debug=True)
