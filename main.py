from flask import Flask, render_template, request, url_for
from bs4 import BeautifulSoup as BS
from item import Item
import json

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


@app.route('/item', methods=['POST'])
def item():
        item_id = request.form['item_id']
        item=Item(item_id)
        json_string=json.dumps([obj.__dict__ for obj in item.reviews],indent=3)
        with open(f'data/{item_id}_reviews.json', 'w') as f:
            f.write(json_string)
        return render_template('item.html', user_data=item.reviews,item_img=item.img,item_name=item.item_name)


if __name__ == '__main__':
    app.run(debug=True)
