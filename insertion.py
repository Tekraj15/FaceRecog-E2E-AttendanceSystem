import pymysql
import pymysql.cursors
import datetime
import cv2
import numpy as np

#def convert(img):
#    ht=img.shape[0]
#    wt=img.shape[1]
#    img=img.reshape(-1)
#    img=np.append(img,[ht,wt])
#    img=np.array(img,dtype=np.uint16)
#    return img


ty=cv2.imread('1.jpg')
picture=cv2.imread('joshva.png')
ht=picture.shape[0]
wt=picture.shape[1]


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='hci')
try:
    with connection.cursor() as cursor:
        sql="insert into head values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,("shas@gmail.com","sa","Joshva","Devdas",pymysql.Binary(picture),ht,wt))
        connection.commit()
finally:
    connection.close()
#try:
#    with connection.cursor() as cursor:
#        sql ="select *from head"
#        cursor.execute(sql)
#        result = cursor.fetchall()
#        l=list(result)
#        img=result[1][2]
#        img=numpy.fromstring(img,dtype='uint8')
#        cv2.imshow(img)
#        print(l[0][0]+l[0][1])
#finally:
#    connection.close()