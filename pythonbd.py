from flask import*

import sqlite3

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/savedetails",methods = ["POST","GET"])
def savedetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees (name, email, address) values (?,?,?)",(name,email,address))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            return render_template("index.html",msg = msg)
            con.close()

@app.route("/view")
def view():
    con = sqlite3.connect("employee.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    ro = cur.fetchall()
    return render_template("view.html",rows = ro)

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where id = ?",id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html",msg = msg)

@app.route("/update")
def update():
    return render_template("update.html");

@app.route("/updatedetails",methods = ["POST","GET"])
def updateDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            id=request.form["id"]
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("Update Employees set name = ?, email = ?,address=? where id = ?",(name,email,address,id))
                con.commit()
                msg = "Employee successfully Updated"
        except:
            con.rollback()
            msg = "We can not update the employee details"
        finally:
            return render_template("index.html",msg = msg)
            con.close()

app.run()