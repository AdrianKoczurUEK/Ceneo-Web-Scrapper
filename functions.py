import glob
import json

def saveAsJs(revs,item_id,obj):
    rev_string=[ob.__dict__ for ob in revs]
    item_data_js={
        'item_id':obj.item_id,
        'item_name':obj.item_name,
        'item_img':obj.img,
        'item_rev_num':obj.rev_num,
        'item_avg_score':obj.item_avg_score,
        'item_pros_count':obj.pros_count,
        'item_cons_count':obj.cons_count,
        'item_reviews':rev_string

    }
    json_string = json.dumps(item_data_js, indent=3)
    with open(f'data/{item_id}.json', 'w') as f:
        f.write(json_string)


def readJsFiles():
    json_data=[]
    paths=glob.glob("data/*.json")
    for path in paths:
        with open(f'{path}', 'r') as f:
            json_dict=json.load(f)
            json_data.append(json_dict)
    return json_data

def getJsonByItemId(item_id):
    with open(f'data/{item_id}.json', 'r') as f:
        return json.load(f)

def sortBy(json_dict_list,sort_by,revers):
    try:
        if revers == 'True':
            revers=True
        else:
            revers=False
        json_dict_list['item_reviews'] = sorted(json_dict_list['item_reviews'], key=lambda x : x[f'{sort_by}'], reverse=revers)
        return json_dict_list
    except:
        return ''