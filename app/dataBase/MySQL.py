import os
import cv2
import pymysql
from PIL import Image

from config.config import Setting

def connect():
    '''
    Commnet : Connect MySQL DataBase
    `
    @parameter : None
    `
    @return : Connection
    '''
    conn = pymysql.connect( 
                        host=Setting.DATABASE_HOST,
                        user=Setting.DATABASE_USER,
                        password=Setting.DATABASE_PWD,
                        db=Setting.DATABASE_DB
                        )

    return conn


def cursorDB(cate, num):
    conn = connect()
    sql_query = createQuery(cate, num)
    curs = conn.cursor()
    curs.execute(sql_query)
    data = curs.fetchall()

    curs.close(), conn.close()

    return data

def getImgList(cate, num):
    '''
    Commnet : Connect MySQL DB and get IMG list
    `
    @parameter : category(select db category), num(select data count(=limit))
    `
    @return : Image Path List [Type : List]
    '''

    base_img_path = Setting.BASE_IMG_PATH

    data = cursorDB(cate, num)

    # change img_path
    imgList = [base_img_path+path+"/"+name for _, path, name in data]
    imgList = checkImgStatus(imgList) #yoloModel.utils.checkImgStatus

    return imgList



def getAllData(cate, num=None):
    '''
    Commnet : Connect MySQL DB and get All DB data
    `
    @parameter : category(select db category), num(select data count(=limit))
    `
    @return : Image Path List [Type : List], DB data [Type : Dict]
    '''

    base_img_path = Setting.BASE_IMG_PATH

    data = cursorDB(cate, num)

    result_dict = {}

    for data in allData:
        line = list(data)
        img_path = f'{base_img_path}{line[7]}/{line[8]}'
        if len(checkImgStatus([img_path])) == 0: continue
        result_dict[img_path] = [line[0], line[1], line[2], line[3], line[5], line[6], img_path, line[9], line[10], line[15]]

    curs.close(), conn.close()

    return result_dict



def checkImgStatus(imgList):
    '''
    Comnet : Image file Validation check
    `
    @parameter : Image Path [Type : List]
    `
    @return : Valid Image Path [Type : List]
    '''
    
    print(f'[DATA] All Data count is {len(imgList)}')
    
    TimgList = []
    for img_path in imgList:
        if not os.path.isfile(img_path): 
            continue
        if cv2.imread(img_path) is None: 
            continue
        try: 
            Image.open(img_path).convert('RGB')
        except: 
            continue
        TimgList.append(img_path)

    print(f'[DATA] After Preproceesing Data count is {len(TimgList)}')

    return TimgList


def createQuery(cate, num):
    if cate == "all":
        if not num:
            sql_query = f'{Setting.BASE_QUERY}'
        else:
            sql_query = f'{Setting.BASE_QUERY} AND LIMIT {str(num)}'
    else:
        if not num:
            sql_query = f'{Setting.BASE_QUERY} AND cat_key="{cate}"'
        else:
            sql_query = f'{Setting.BASE_QUERY} AND cat_key="{cate}" LIMIT {str(num)}'
    
    print(f'[SQL] {sql_query}')

    return sql_query
