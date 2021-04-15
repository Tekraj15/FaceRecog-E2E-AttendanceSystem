import pymysql
import pymysql.cursors
import datetime
import cv2
import numpy
ty=cv2.imread('1.jpg')
now=datetime.datetime.utcnow()

def convert(img,ht,wt):
    img=img.reshape(ht,wt,3)
    return img


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='hci')
try:
    with connection.cursor() as cursor:
        sql ="select *from students"
        cursor.execute(sql)
        result = cursor.fetchall()
        l=list(result)
        img=result[0][5]
        img=numpy.fromstring(img,dtype='uint8')
        ht=result[0][6]
        wt=result[0][7]
        img=convert(img,ht,wt)
        cv2.imshow("Person",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(l[0][0]+l[0][1])
finally:
    connection.close()