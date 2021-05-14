from flask import Flask,render_template,request,redirect,url_for,session
import cv2
import numpy as np
import pymysql
import pymysql.cursors
from werkzeug.utils import secure_filename
import os
import all_present
import all_absent
import combine
import shutil


UPLOAD_FOLDER = r'C:\Users\Shaswat\Desktop\HCI -3\static\images\dump'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def status(a):
    if(a==0):
        return "Absent"
    return "Present"

def convert(img,ht,wt):
    img=img.reshape(ht,wt,3)
    return img


def pre_process(result):
    path=r"C:\Users\Shaswat\Desktop\HCI -3\static\images\Attendance/"
    w=[]
    for i in range(len(result)):
        l=[]
        fname=result[i][0]
        lname=result[i][1]
        name=fname+" "+lname
        img=np.fromstring(result[i][5],dtype='uint8')
        img=convert(img,result[i][6],result[i][7])
        p=path+name+".jpg"
        cv2.imwrite(p,img)
        p="images/Attendance/"+name+".jpg"
        l.extend([name,result[i][2],p,status(result[i][4])])
        w.append(l)
    return w
    


app= Flask(__name__)
app.secret_key = "abc"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/')
def index():
    path=r"C:\Users\Shaswat\Desktop\HCI -3\static\images\Attendance"
    try:
        shutil.rmtree(path)
        shutil.rmtree(UPLOAD_FOLDER)
    except:
        print("Already Created")
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    session.clear()
    return render_template("index.html")



@app.route("/register")
def register():
    return render_template("signup.html")




@app.route('/handle',methods=["POST"])
def handle():
    cv2.destroyAllWindows()
    if(session.get("teacher") or request.form.get("teacher")):
        if(session.get("email") and session.get("pass")):
            email=session["email"]
            pas=session["pass"]
        else:
            email=request.form["email"]
            pas=request.form["pass"]
            session["email"]=email
            session["pass"]=pas
            session["teacher"]="teacher"
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='hci')
        with connection.cursor() as cursor:
            sql = "SELECT * from head where email=%s and pass=%s"
            cursor.execute(sql,(email,pas))
            result = cursor.fetchall()
            if(len(result)==0):
                return render_template("index3.html")
            else:

                fname=result[0][2]
                lname=result[0][3]
                name=fname+" "+lname
                img=result[0][4]
                img=np.fromstring(img,dtype='uint8')
                ht=result[0][5]
                wt=result[0][6]
                img=convert(img,ht,wt)
                cv2.imwrite(r"C:\Users\Shaswat\Desktop\HCI -3\static\images\dump\Person.jpg",img)
                
                with connection.cursor() as cursor:
                    sql = "SELECT * from students order by f_name,l_name"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if(len(result)==0):
                        return render_template("login.html",nam=name,len=0,details=[[]])
                    else:
                        w=pre_process(result)
                        return render_template("login.html",nam=name,len=len(w),details=w)
    else:
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='hci')
        email=request.form["email"]
        pas=request.form["pass"]
        with connection.cursor() as cursor:
            sql = "SELECT * from students where email=%s and pass=%s"
            cursor.execute(sql,(email,pas))
            result = cursor.fetchall()
            if(len(result)==0):
                return render_template("index3.html")
            else:
                img=result[0][5]
                img=np.fromstring(img,dtype='uint8')
                ht=result[0][6]
                wt=result[0][7]
                img=convert(img,ht,wt)
                cv2.imwrite(r"C:\Users\Shaswat\Desktop\HCI -3\static\images\dump\Person.jpg",img)
                return render_template("student.html",nam=(result[0][0]+" "+result[0][1]),stat=status(result[0][4]))
                
        
    
@app.route('/signup',methods=["POST"])
def signup():   
    try:
        file=request.files.get("file")
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        picture=cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ht=picture.shape[0]
        wt=picture.shape[1]
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='hci')
        try:
            with connection.cursor() as cursor:
                sql="insert into students values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(request.form["F_name"],request.form["L_name"],request.form["email"],request.form["password"],0,pymysql.Binary(picture),ht,wt))
                connection.commit()
                return render_template("index2.html")
        finally:
            connection.close()
    except Exception as e:
        print(e)
        return redirect(url_for('register'))
    




@app.route('/attendance',methods=["POST"])
def attendance():
    if(request.form.get("present")==""):
        all_present.present()
        return redirect(url_for('handle'),code=307)
    elif(request.form.get("absent")==""):
        all_absent.absent()
        return redirect(url_for('handle'),code=307)
    elif(request.form.get("start")==""):
        combine.attend()
        return redirect(url_for("handle"),code=307)
#        



if __name__=="__main__":
    app.run(use_reloader=False,debug=True)