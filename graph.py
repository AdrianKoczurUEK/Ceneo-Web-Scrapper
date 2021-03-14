import matplotlib.pyplot as plt

import base64
from io import BytesIO


def plot_stars(stars):
    fig,ax  = plt.subplots(figsize=(5,5))
    plt.title("Opinie")
    plt.ylabel("Ocena")
    plt.xlabel("Ilość")
    plt.barh(*zip(*stars.items()),color=['#FC4444', '#FC8A44', '#FCEE44', '#ECFC44', '#CAFC44', '#A4FC44'])
    for index, value in enumerate(stars.values()):
        plt.text(value+0.5 if value < 5 else value/2-1 , index, str(value),fontsize=8)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    return format(encoded)

def plot_recommend(recommend):
    fig,ax  = plt.subplots(figsize=(5,5))
    plt.title("Opinie")
    plt.pie(recommend.values(),colors=['#62C60D','#F14949'],explode=(0,0.15) if list(recommend.values())[1] >0 else (0,0),shadow=True,autopct='%1.1f%%',startangle=70)
    ax.legend(recommend.keys())
    ax.axis('equal')
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    return format(encoded)

def get_stars(json):
    stars={
        '0':0,
        '1':0,
        '2':0,
        '3':0,
        '4':0,
        '5':0
    }
    for rev in json['item_reviews']:
        try:
            stars[rev['stars'].split("/")[0]]+=1
        except:
            stars[rev['stars'].split("/")[0].split(",")[0]] += 1

    return stars

def get_recommends(json):
    recommends = {
        'Polecam': 0,
        'Nie polecam': 0
    }

    for rev in json['item_reviews']:
        try:
            recommends[rev['recommended']]+=1
        except:
            pass
    return recommends


def generate_stars_plot(item_json):
    stars=get_stars(item_json)
    return plot_stars(stars)

def generate_recommend_plot(item_json):
    recommends=get_recommends(item_json)
    return plot_recommend(recommends)


