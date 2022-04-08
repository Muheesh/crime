from flask import Flask, request, render_template, session
import sqlite3

from flask_session import Session
from werkzeug.utils import redirect
from datetime import date

data = sqlite3.connect("report.db",check_same_thread=False)
table1 = data.execute("select * from sqlite_master where type = 'table' and name = 'crime'").fetchall()
table2 = data.execute("select * from sqlite_master where type = 'table' and name = 'user'").fetchall()
if table1!=[]:
    print("Crime table already exists")
else:
    data.execute('''create table crime(
                            id integer primary key autoincrement,
                            description text,
                            remarks text,
                            date text);''')
    print("Table created")
if table2!=[]:
    print("Crime table already exists")
else:
    data.execute('''create table user(
                            id integer primary key autoincrement,
                            name text,
                            address text,
                            email text,
                            phone integer,
                            password text);''')
    print("User Table created")

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/',methods=['GET','POST'])
def Login_admin():
    if request.method == 'POST':
        getUsername = request.form["name"]
        getPassword = request.form["pass"]
        print(getUsername)
        print(getPassword)
        if getUsername == "admin" and getPassword == "12345":
            return redirect('/dashboard')
        else:
            return redirect('/')
    return render_template("adminlogin.html")

@app.route('/dashboard')
def Admin_dashboard():
    return render_template("admindash.html")

@app.route('/view')
def View_report():
    cursor = data.cursor()
    count = cursor.execute("select * from crime")

    result = cursor.fetchall()
    return render_template("view.html",crime=result)


@app.route('/sort',methods=['GET','POST'])
def Search_crime():
    if request.method == 'POST':
        getDate = request.form["date"]
        cursor = data.cursor()
        count = cursor.execute("select * from crime where date="+getDate)
        result = cursor.fetchall()
        if result is None:
            print("There is no Crime on",getDate)
        else:
            return render_template("sortdate.html",search=result,status=True)
    else:
        return render_template("sortdate.html",search=[],status=False)



@app.route('/register',methods=['GET','POST'])
def User_register():
    if request.method == 'POST':
        getName = request.form["name"]
        getAddress = request.form["address"]
        getEmail = request.form["email"]
        getPhone = request.form["phone"]
        getPass = request.form["pass"]
        try:
            data.execute("insert into user(name,address,email,phone,password) \
            values('"+getName+"','"+getAddress+"','"+getEmail+"',"+getPhone+",'"+getPass+"')")
            data.commit()
            return redirect('/complaint')
        except Exception as err:
            print(err)
    return render_template("register.html",status=True)

@app.route('/user',methods=['GET','POST'])
def Login_user():
    if request.method == 'POST':
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        cursor = data.cursor()
        query = "select * from user where email='"+getEmail+"' and password='"+getPass+"' "
        result = cursor.execute(query).fetchall()
        if len(result)>0:
            for i in result:
                getName = i[1]
                getId = i[0]
                session["name"] = getName
                session["id"] = getId
            return redirect('/complaint')
        else:
            return render_template("userlogin.html",status=True)
    else:
        return render_template("userlogin.html",status=False)

@app.route('/userpage')
def userpage():
    if not session.get("name"):
        return redirect('/')
    else:
        return render_template("userpage.html")


@app.route('/complaint',methods=['GET','POST'])
def report_crime():
    if request.method == 'POST':
        getDescrip = request.form["description"]
        getRemark = request.form["remark"]
        getDate = date.today()
        cursor = data.cursor()
        cursor.execute("insert into crime(description,remarks) values('"+getDescrip+"','"+getRemark+"','"+getDate+"')")
        data.commit()
        print("Inserted Successfully")
        return redirect('/')
    return render_template("complaint.html")

@app.route('/update',methods=['GET','POST'])
def Update_user():
    global getUser
    if request.method == 'POST':
        getUser = request.form["name"]
        cursor = data.cursor()
        count = cursor.execute("select * from user where name="+getUser)
        return redirect('/edit')
    return render_template("update.html",status=True)


@app.route('/edit',methods=['GET','POST'])
def User_edit():
    if request.method == 'POST':
        getName = request.form["name"]
        getAddress = request.form["address"]
        getEmail = request.form["email"]
        getPhone = request.form["phone"]
        getPass = request.form["pass"]
        data.execute("update user set name='"+getName+"',address='"+getAddress+"',email='"+getEmail+"',phone="+getPhone+",password='"+getPass+"' where name='"+getUser+"'")
        data.commit()
        return redirect('/user')

    return render_template("edituser.html")

@app.route('/logout')
def Logout():
    session["name"] = None
    return redirect('/')



if __name__=="__main__":
    app.run()