import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
from flask import*
app=Flask(__name__)
app.secret_key="aaa"
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'safacollegeproject2022@gmail.com'
app.config['MAIL_PASSWORD'] = 'safacollegeproject2022@gmail'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



from  src.dbconnection import *

@app.route('/login',methods=['post'])
def login():
    uname=request.form['uname']
    pswd=request.form['password']
    qry="select * from login where Username=%s and Password=%s AND TYPE='student'"
    val=(uname,pswd)
    res=selectone(qry,val)
    if res is None:
        return jsonify({'task':'invalid'})
    else:
        return jsonify({'task': 'success','id':res[0]})



@app.route('/register', methods=['post'])
def reg():

     try:
        print(request.form)
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        dob = request.form['dob']
        weight = request.form['weight']
        course=request.form['course']
        sem = request.form['sem']
        phonno = request.form['phone']
        blood= request.form['blood']
        ldd = request.form['lastdon']
        uname=request.form['uname']
        pwd=request.form['pwd']
        email=request.form['email']
        place = request.form['place']
        post=request.form['post']

        pin = request.form['pin']

        qry = "INSERT INTO `login` VALUES(NULL,%s,%s,'student')"
        val = (uname,pwd)
        s = iud(qry, val)
        qry="insert into `student` values(Null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(str(s),fname,lname,gender,dob,place,post,pin,weight,course,sem,phonno,blood,ldd)
        iud(qry,val)
        qry="INSERT INTO email VALUES(NULL,%s,%s)"
        val=(str(s),email)
        iud(qry, val)
        return jsonify({'task': 'success'})
     except Exception as e:
        print(e)
        return jsonify({'task': 'error'})




@app.route('/changepassword',methods=['post'])
def changepassword():
    login_id = request.form['lid']
    current = request.form['current']
    new = request.form['newp']
    qry="SELECT * FROM `login` WHERE `Password`=%s AND `Login_id`=%s"
    val=(current,login_id)
    res=selectone(qry,val)
    if res is not None:

        qry="UPDATE login SET `Password`=%s WHERE `Login_id`=%s"
        val=(new,login_id)
        iud(qry,val)

        return jsonify({'task': 'success'})
    else:
        return jsonify({'task': 'error'})










@app.route('/update_profile',methods=['post'])
def update_profile():
    print(request.form)
    login_id=request.form['lid']
    fname=request.form['fname']
    lname=request.form['lname']
    gender=request.form['gender']
    dob=request.form['dob']
    weight=request.form['weight']
    sem=request.form['sem']
    phonno=request.form['phonno']
    ldd=request.form['ldd']
    blood=request.form['blood']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email=request.form['email']
    qry="UPDATE student SET `First_name`=%s,`Last_name`=%s,`Gender`=%s,`Date_Of_Birth`=%s,place=%s,post=%s,pin=%s,`Weight`=%s,`Semester`=%s,`Phone_No`=%s,Blood_Group=%s,`Last_donate_date`=%s WHERE `Login_id`=%s"
    val=(fname,lname,gender,dob,place,post,pin,weight,sem,phonno,ldd,blood,login_id)
    iud(qry,val)
    qry = "UPDATE `email` SET email=%s WHERE uid=%s"
    val = (email,login_id)
    iud(qry, val)
    return jsonify({'task': 'success'})

@app.route('/viewcampdetails',methods=['post'])
def viewcampdetails():
    qry="SELECT * FROM `campdetails`"
    res=androidselectallnew(qry)
    return jsonify(res)

@app.route('/viewnotification',methods=['post'])
def viewnotification():
    qry = "SELECT * FROM `notification`"
    res = androidselectallnew(qry)
    return jsonify(res)

@app.route('/addrating',methods=['post'])
def addrating():
    sid=request.form['lid']
    feedback=request.form['feedback']
    rating=request.form['rating']
    qry="insert into feedback values(null,%s,%s,%s,curdate())"
    val=(sid,feedback,rating)
    iud(qry,val)
    return jsonify({'task': 'success'})

@app.route('/viewbloodgroup',methods=['post'])
def viewbloodgroup():
    id=request.form['lid']
    lati=request.form['lati']
    longi=request.form['longi']
    group=request.form['group']
    qry = "SELECT `student`.*, (3959 * ACOS ( COS ( RADIANS(%s) ) * COS( RADIANS( `locaion`.lattitude) ) * COS( RADIANS( `locaion`.longitude ) - RADIANS(%s) ) + SIN ( RADIANS(%s) ) * SIN( RADIANS( `locaion`.lattitude ) ))) AS user_distance FROM `student` JOIN `locaion` ON `locaion`.`student_id`=`student`.`Login_id` WHERE `student`.`Blood_Group`=%s AND `Login_id`!=%s HAVING user_distance  < 31.068"
    val=(lati,longi,lati,group,id)
    res = androidselectall(qry,val)
    return jsonify(res)

@app.route('/loc',methods=['post'])
def loc():
    print(request.form)
    lat=request.form['lati']
    lon=request.form['longi']
    id=request.form['lid']
    qry="SELECT * FROM `locaion` WHERE `student_id`=%s"
    res=selectone(qry,id)
    if res is None:
        qry="INSERT INTO `locaion` VALUES(NULL,%s,%s,%s)"
        val=(id,lat,lon)
        iud(qry,val)
    else:
        qry="UPDATE `locaion` SET `lattitude`=%s,`longitude`=%s WHERE `student_id`=%s"
        val=(lat,lon,id)
        iud(qry,val)

    return jsonify({'task': 'success'})






@app.route('/view_rating',methods=['post'])
def view_rating():
    id=request.form['lid']
    qry = "SELECT * FROM `feedback` WHERE `Student_id`=%s"
    res = androidselectall(qry,id)
    return jsonify(res)




@app.route("/viewprofile",methods=['post'])
def viewprofile():
    id=request.form['lid']
    qry="SELECT student.*,`email`.email FROM student JOIN email ON email.uid=student.Login_id WHERE student.Login_id=%s"
    res=androidselectall(qry,id)
    return jsonify(res)






@app.route('/fgtpwd',methods=['post'])
def fgtpwd():
    print(request.form)
    try:
        print(request.form)
        email=request.form['email']
        print(email)
        qry="SELECT `login`.`password` FROM `email`  JOIN `login` ON `login`.`Login_id` = `email`.`uid` WHERE email=%s"
        s = selectone(qry,email)
        print(s,"=============")
        if s is None:
            return jsonify({'task': 'invalid email'})
        else:
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('safacollegeproject2022@gmail.com', 'safacollegeproject2022@gmail')
            except Exception as e:
                print("Couldn't setup email!!" + str(e))
            msg = MIMEText("Your new password id : " + str(s[0]))
            print(msg)
            msg['Subject'] = 'Eblood Password'
            msg['To'] = email
            msg['From'] = 'safacollegeproject2022@gmail.com'
            try:
                gmail.send_message(msg)
            except Exception as e:
                print("COULDN'T SEND EMAIL", str(e))
            return jsonify({'task': 'success'})
    except:
        return jsonify({'task': 'error'})


















if __name__ =="__main__":
    app.run(host="0.0.0.0",port=5000)
