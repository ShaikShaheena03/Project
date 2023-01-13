from flask import Flask,redirect,render_template,url_for,request,jsonify
from flask_mysqldb import MySQL
from secretconfig import secret_key
from py_mail import mail_sender
import smtplib
from email.message import EmailMessage
 
app=Flask(__name__)
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']='@06Sep2003'
app.config['MYSQL_DB']='RESULTS'
mysql=MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student',methods=['GET','POST'])
def student():
    if request.method=='POST':
        student=request.form['student']
        section=request.form['section1']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * from marks where stud_id=%s',[student])
        data=cursor.fetchall() 
        cursor.close()
        if student==student:
            return redirect(url_for('final'))
        else:
            return render_template('student.html')
    return render_template('student.html')

@app.route('/finalcertificate',methods=['GET','POST'])
def final():
    if request.method=='POST':
        student=request.form['student']
        cursor=mysql.connection.cursor()    
        cursor.execute("SELECT count(*) from marks where stud_id=%s",[student])
        count=int(cursor.fetchone()[0])
        cursor.close()
        if count==0:
            return render_template('final.html',student='empty')
        else:
            cursor=mysql.connection.cursor()    
            cursor.execute("SELECT count(*) from marks where stud_id=%s",[student])
            count=cursor.fetchall()
            cursor.close()
             return render_template('final.html',student=count)
    return render_template('final.html',student=count

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        user=request.form['userName']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT userName,password from admin where userName=%s',[user])
        data=cursor.fetchall()[0]
        user=data[0]
        password=data[1]
        cursor.close()
        if user==user and password==password:
            return redirect(url_for('addstudents'))
        else:
            return render_template('adminlogin.html')
    return render_template('adminlogin.html')
@app.route('/signin',methods=['GET','POST'])
def signin():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT count(*) from admin')
    result=int(cursor.fetchone()[0])
    cursor.close()
    if request.method=='POST':
        key=request.form['secret']
        name=request.form['fname']
        username=request.form['user']
        email=request.form['mail']
        number=request.form['phone']
        password=request.form['password']
        passcode=request.form['passcode']
        gender=request.form['gender']
        if key!=secret_key:
            return '''<h1>Account Creation Failed:Wrong secret key</h1>'''
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('insert into admin values(%s,%s,%s,%s,%s,%s,%s,%s)',[key,name,username,email,number,password,passcode,gender])
            mysql.connection.commit()
            return redirect(url_for('adminlogin'))     
    return render_template('signin.html')

@app.route('/addsubjects',methods=['GET','POST'])
def addsubjects():
    if request.method=='POST':
        section=request.form['section']
        courseid=request.form['course']
        subjectName=request.form['subjectName']
        totalMarks=request.form['totalMarks']
        cursor=mysql.connection.cursor()
        #query=f"insert into {section} (subject,total_marks) values('{subjectName}',{totalMarks})"
        cursor.execute('insert into subjects(section,course_id,subject,total_marks) values(%s,%s,%s,%s)',[section,courseid,subjectName,totalMarks])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('addsubjects'))
    return render_template('addsubjects.html')

@app.route('/addstudents',methods=['GET','POST'])
def addstudents():
    if request.method=='POST':
        studentId=request.form['studentId']
        studentName=request.form['studentName']
        fatherName=request.form['fatherName']
        motherName=request.form['motherName']
        phoneNumber=request.form['phoneNumber']
        address=request.form['address']
        emailId=request.form['emailId']
        adharNumber=request.form['adharNumber']
        gender=request.form['gender']
        section=request.form['section']
        cursor=mysql.connection.cursor()
        cursor.execute('insert into students(studentId,studentName,fatherName,motherName,phoneNumber,address,emailId,adharNumber,gender,section) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[studentId,studentName,fatherName,motherName,phoneNumber,address,emailId,adharNumber,gender,section])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('addstudents'))
    return render_template('addstudents.html')

@app.route('/addresult',methods=['GET','POST'])
def addresult():
    cursor=mysql.connection.cursor()
    cursor.execute('select subject from subjects')
    data=cursor.fetchall()
    '''cursor=mysql.connection.cursor()
    cursor.execute('select subject from msds2')
    data1=cursor.fetchall()
    cursor=mysql.connection.cursor()
    cursor.execute('select subject from msds3')
    data2=cursor.fetchall()'''
    subjects=data 
    if request.method=='POST':
        studentId=request.form['student']
        subject=request.form['subject']
        obtainedMarks=request.form['obtained']
        cursor=mysql.connection.cursor()
        cursor.execute('insert into marks(stud_id,subject,obtained) values(%s,%s,%s)',[studentId,subject,obtainedMarks])
        mysql.connection.commit()
        cursor.close()
        return render_template('addresult.html' ,subjects=subjects)
    return render_template('addresult.html',subjects=subjects)

@app.route('/viewstudent',methods=['GET','POST'])
def viewstudent():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from students')
    students=cursor.fetchall()
    cursor.close()
    return render_template('viewstudent.html',students=students)

@app.route('/studentsearch',methods=['POST'])
def studentsearch():
    if request.method=='POST':
        students=request.form['studentId']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from students where studentId=%s',[students])
        count=int(cursor.fetchone()[0])
        cursor.close()
        if count==0:
            return render_template('searchbar_students.html',students='empty')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('select * from students where studentId=%s',[students])
            count=cursor.fetchall()
            cursor.close()
            return render_template('searchbar_students.html',students=count)
    return render_template('searchbar_students.html',students=count)

@app.route('/deletestudent',methods=['POST'])
def deletestudent():
    if request.method=='POST':
        print(request.form)
        student=request.form['option'].split()
        cursor=mysql.connection.cursor()
        cursor.execute('delete from students where studentId=%s',[student[0]])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewstudent'))
    
@app.route('/viewsubject')
def viewsubject():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * from subjects")
    subjects=cursor.fetchall()
    cursor.close()
    return render_template('viewsubject.html',subjects=subjects)


@app.route('/subjectsearch',methods=['GET','POST'])
def subjectsearch():
    if request.method=='POST':
        course=request.form['course']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from subjects where course_id=%s',[course])
        count=int(cursor.fetchone()[0])
        cursor.close()
        if count==0:
            return render_template('searchbar_subjects.html',course='empty')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('select * from subjects where course_id=%s',[course])
            count=cursor.fetchall()
            cursor.close()
            return render_template('searchbar_subjects.html',course=count)
    return render_template('searchbar_subjects.html',course=count)

@app.route('/deletesubject',methods=['POST'])
def deletesubject():
    if request.method=='POST':
        print(request.form)
        course=request.form['option1'].split()
        cursor=mysql.connection.cursor()
        cursor.execute('delete from subjects where course_id=%s',[course[0]])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewsubject'))
        
@app.route('/viewresult',methods=['GET','POST'])
def viewresult():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from marks')
    marks=cursor.fetchall()
    cursor.close()
    return render_template('viewresult.html',marks=marks)

@app.route('/resultsearch',methods=['POST'])
def resultsearch():
    if request.method=='POST':
        studentid=request.form['studentId']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from marks where stud_id=%s',[studentid])
        count=int(cursor.fetchone()[0])
        cursor.close()
        if count==0:
            return render_template('searchbar_result.html',studentid='empty')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('select * from marks where stud_id=%s',[studentid])
            count=cursor.fetchall()
            cursor.close()
            return render_template('searchbar_result.html',studentid=count)
        return render_template('searchbar_result.html',studentid=count)
        
@app.route('/deleteresult',methods=['POST'])
def deleteresult():
    if request.method=='POST':
        print(request.form)
        subject=request.form['option2'].split()
        cursor=mysql.connection.cursor()
        cursor.execute('delete from marks where stud_id=%s',[subject[0]])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewresult'))

app.run(debug=True)
