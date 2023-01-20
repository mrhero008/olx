from flask import Flask, render_template, request, redirect, url_for
from models import *
from ast import literal_eval as le
import requests
from datetime import datetime
from werkzeug.utils import secure_filename
import os

setcookie = "https://httpbin.org/cookies/set"
getcookie = "https://httpbin.org/cookies"
s = requests.Session()
s.get(setcookie, params={"login": "False"})
s.get(setcookie, params={"id": ""})

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/media"


@app.route("/")
def homepage():
    return render_template("index.html", e=le(s.get(getcookie).text)["cookies"]["id"], tek=le(s.get(getcookie).text)["cookies"]["login"], all=Products.select())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form.get("login"):
            login = request.form.get("email")
            password = request.form.get("password")
            if login == "admin@bk.ru" and password == "joxamanj1":
                s.get(setcookie, params={"login": True})
                s.get(setcookie, params={"id": "admin@bk.ru"})
                return redirect("/admin")
            else:
                info = Users.select().where(Users.email == login, Users.password == password)
                if len(info) == 0:
                    return render_template("login.html", e=le(s.get(getcookie).text)["cookies"]["id"], tek=le(s.get(getcookie).text)["cookies"]["login"], disp="block", content="Login yoki parol xato")
                else:
                    s.get(setcookie, params={"login": True})
                    s.get(setcookie, params={"id": info[0].email})
                    return redirect("/")
        else:
            login = request.form.get("email")
            password = request.form.get("password")
            info = Users.select().where(Users.email == login)
            if len(info) == 0:
                try:
                    new_user = Users(email=login, password=password)
                    new_user.save()
                    return redirect("/login#login", tek=le(s.get(getcookie).text)["cookies"]["login"])
                except:
                    return render_template("login.html", e=le(s.get(getcookie).text)["cookies"]["id"], tek=le(s.get(getcookie).text)["cookies"]["login"], disp="block", content="Ro'yxatdan o'tib bo'lmadi. Qayta urunib ko'ring")
            else:
                return redirect("/login")
    else:
        if le(s.get(getcookie).text)["cookies"]["login"] == "True":
            return redirect("/")
        else:
            return render_template("login.html", e=le(s.get(getcookie).text)["cookies"]["id"], disp="none", tek=le(s.get(getcookie).text)["cookies"]["login"], content="")


def allowed_file(filenam):
    if filenam.split('.')[-1] in ALLOWED_EXTENSIONS:
        return filenam


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        description = request.form.get("description")
        kategory = request.form.get("kategory")
        city = request.form.get("city")
        name = request.form.get("name")
        price = request.form.get("price")
        date = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
        time = f"{datetime.now().hour}:{datetime.now().minute}"
        image = request.files.get("image")
        print(image)
        if image == "":
            image = "no.jpg"
        elif allowed_file(image.filename):
            imgname = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], imgname))
        Products(name=name, email=email, number=number, image=secure_filename(image.filename),
                 description=description, kategory=kategory, city=city, date=date, time=time, price=price).save()
        return redirect("/")

    if le(s.get(getcookie).text)["cookies"]["login"] == "True":
        return render_template("add.html", e=le(s.get(getcookie).text)["cookies"]["id"], email=le(s.get(getcookie).text)["cookies"]["id"], tek=le(s.get(getcookie).text)["cookies"]["login"])
    else:
        return redirect("/login")


@app.route("/kategory", methods=["GET", "POST"])
def kategory():
    k = request.args.get("k")
    all = Products.select().where(Products.kategory == k)
    print(k)
    return render_template("kategory.html", tek=le(s.get(getcookie).text)["cookies"]["login"], e=le(s.get(getcookie).text)["cookies"]["id"], all=all, le=len(all))


@app.route("/full", methods=["POST", "GET"])
def full():
    id = request.args.get("id")
    all = Products.select().where(Products.id == id)[0]
    return render_template("full.html", e=le(s.get(getcookie).text)["cookies"]["id"], info=all, tek=le(s.get(getcookie).text)["cookies"]["login"])


@app.route("/upload/<filename>")
def get_image(filename):
    return url_for("static", filename="media/" + filename)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        k = request.args.get("search")
        al = Products.select().where(Products.name.contains(k))
        return render_template("kategory.html", e=le(s.get(getcookie).text)["cookies"]["id"], all=al, le=len(al), tek=le(s.get(getcookie).text)["cookies"]["login"])


@app.route("/admin")
def admin():
    if le(s.get(getcookie).text)["cookies"]["id"] == "admin@bk.ru":
        return render_template("admin.html", e=le(s.get(getcookie).text)["cookies"]["id"], users=Users.select(), products=Products.select(), tek=le(s.get(getcookie).text)["cookies"]["login"])
    else:
        return redirect("/")


@app.route("/delet")
def delet():
    if le(s.get(getcookie).text)["cookies"]["id"] == "admin@bk.ru":
        id = request.args.get("id")
        u = Users.get(Users.id == id)
        Products.get(Products.email == u.email).delete_instance()
        u.delete_instance()
        return redirect("/admin")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    s.get(setcookie, params={"login": "False"})
    s.get(setcookie, params={"id": ""})
    return redirect("/login")


@app.route("/myproducts")
def myproducts():
    if le(s.get(getcookie).text)["cookies"]["login"] == "True":
        all = Products.select().where(Products.email == le(
            s.get(getcookie).text)["cookies"]["id"])
        return render_template("myproducts.html", all=all, e=le(s.get(getcookie).text)["cookies"]["id"], email=le(s.get(getcookie).text)["cookies"]["id"], tek=le(s.get(getcookie).text)["cookies"]["login"])
    else:
        return redirect("/login")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        name = request.form.get("name")
        id = request.form.get("id")
        email = request.form.get("email")
        number = request.form.get("number")
        description = request.form.get("description")
        kategory = request.form.get("kategory")
        city = request.form.get("city")
        name = request.form.get("name")
        price = request.form.get("price")
        date = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
        time = f"{datetime.now().hour}:{datetime.now().minute}"
        image = request.files.get("image")
        print(image)
        if image == "":
            image = "no.jpg"
        elif allowed_file(image.filename):
            imgname = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], imgname))
        pr = Products.get(Products.id == id)
        pr.name = name
        pr.image = secure_filename(image.filename)
        pr.email = email
        pr.number = number
        pr.description = description
        pr.kategory = kategory
        pr.city = city
        pr.price = price
        pr.date = date
        pr.time = time
        pr.save()

        return redirect("/")

    if le(s.get(getcookie).text)["cookies"]["login"] == "True":
        id = request.args.get("id")
        directory = os.getcwd()
        al = Products.select().where(Products.id == id)
        return render_template("edit.html", dir=directory, all=al[0], e=le(s.get(getcookie).text)["cookies"]["id"], email=le(s.get(getcookie).text)["cookies"]["id"], tek=le(s.get(getcookie).text)["cookies"]["login"])
    else:
        return redirect("/login")


app.run(debug=True, port="7777")
