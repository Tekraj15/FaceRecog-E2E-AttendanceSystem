import mysql.connector
import datetime
import cv2
import numpy as np

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

picture2 = cv2.imread(r"C:\Users\Shaswat\Desktop\Microsoft-intership\12th marksheet.jpg")



imcv=cv2.imread(r'C:\Users\Shaswat\Desktop\HCI -3\static\images\dump\12th_marksheet.jpg')


now=datetime.datetime.utcnow()
#image=np.array(img,dtype=np.float64)
connection = mysql.connector.connect(host='localhost',
                             user='root',
                             password='',
                             db='hci')
try:
    cursor=connection.cursor()
    sql = "INSERT INTO head VALUES (%s,%s,%s)"
    cursor.execute(sql,("shas","sa",picture))
    connection.commit()

finally:
    connection.close()