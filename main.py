from flask import Flask, render_template, request, send_file
from functions import readJsFiles, saveAsJs
from item import Item

app = Flask(__name__)
@app.route('/list')
def item_list():
    items_data=readJsFiles()
    return render_template('item_list.html',page='list',items_data=items_data)

@app.route('/download', methods=['POST'])
def downloadFile ():
    path = request.form['downloadJson']
    return send_file(path, as_attachment=True)

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
        saveAsJs(item.reviews,item_id,item)
        return render_template('item.html', user_data=item.reviews,item_img=item.img,item_name=item.item_name)


if __name__ == '__main__':
    app.run(debug=True)
