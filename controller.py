from flask import Flask, render_template, request, redirect
from datetime import datetime
import pymysql
import models as mdls
import user
import ast

app = Flask(__name__)


id_user = None
user_name = None
cart_local = []


@app.route("/")
def index():
    global id_user
    return render_template("index.html", id_user=id_user)


@app.route("/logout")
def logout():
    global user_name
    user_name = None
    global id_user
    id_user = None
    return redirect("/", code=302, Response=None)


@app.route("/catalog")
def catalog():
    global id_user
    car_list = mdls.get_cars_from_db()
    return render_template("catalog.html", car_list=car_list, id_user=id_user)


@app.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        id_car = int(request.form.get('id_car'))
        id_user = request.form.get('id_user')
        if not id_user or id_user == 'None':
            car_in_cart = False
            global cart_local
            for car in cart_local:
                if car["id_car"] == id_car:
                    car["car_count"] = car["car_count"] + 1
                    car_in_cart = True
            if not car_in_cart:
                cart_local.append({
                    "id_car": id_car,
                    "car_count": 1,
                })
        else:
            mdls.add_car_in_cart(id_car, id_user)
    return redirect("/", code=302, Response=None)


@app.route("/edit/<id>", methods=['POST', 'GET'])
def edit(id):
    car_list = mdls.get_cars_from_db()
    if request.method == 'GET':
        for car in car_list:
            if car["id"] == int(id):
                return render_template("edit.html", car=car)
    elif request.method == 'POST':
        new_price = request.form.get('price')
        mdls.change_price(id, new_price)
        return redirect("/catalog", code=302, Response=None)


@app.route("/delete/<id>")
def delete(id):
    mdls.delete_car(id)
    return redirect("/catalog", code=302, Response=None)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        global id_user
        global user_name
        id_user, user_name = user.login()
        if id_user:
            global cart_local
            if cart_local:
                for car in cart_local:
                    id_car = car["id_car"]
                    mdls.add_car_in_cart(id_car, id_user, car["car_count"])
                cart_local = []
            return redirect("/", code=302, Response=None)
        return redirect("/login", code=302, Response=None)


@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")
    elif request.method == 'POST':
        global id_user
        global user_name
        id_user, user_name = user.signin()
        if id_user:
            global cart_local
            if cart_local:
                for car in cart_local:
                    id_car = car["id_car"]
                    mdls.add_car_in_cart(id_car, id_user, car["car_count"])
                cart_local = []
            return redirect("/", code=302, Response=None)
        return redirect("/signin", code=302, Response=None)


@app.route("/contacts")
def contacts():
    global id_user
    return render_template("contacts.html", id_user=id_user)


@app.route("/cart")
def cart():
    global cart_local
    global id_user
    car_list = []

    if not id_user or id_user == 'None':
        for i, car in enumerate(cart_local):
            car_list.append(mdls.get_car_by_id_from_db(car["id_car"]))
            car_list[i]["car_count"] = car["car_count"]
    else:
        car_list = mdls.get_car_list_in_cart(id_user)
    return render_template("cart.html", car_list=car_list, id_user=id_user)

@app.route("/update_count", methods=['POST'])
def update_count():
    global cart_local
    id_user = request.form.get('id_user')
    id_car = int(request.form.get('id_car'))
    car_count = int(request.form.get('car_count'))
    car_list = []

    if not(id_user) or id_user == 'None':
        for i, car in enumerate(cart_local):
            if car["id_car"] == id_car:
                car["car_count"] = car_count
            car_list.append(mdls.get_car_by_id_from_db(car["id_car"]))
            car_list[i]["car_count"] = car["car_count"]
    else:
        car_list = mdls.get_car_list_in_cart(id_user)
        for car in car_list:
            if car["id"] == id_car:
                old_car_count = car["car_count"]
                add_car_count = car_count - old_car_count
                mdls.add_car_in_cart(id_car, id_user, add_car_count)
    return render_template("cart.html", car_list=car_list, id_user=id_user)


@app.route("/make_order", methods=["POST"])
def make_order():
    id_user = int(request.form.get('id_user'))
    car_list = ast.literal_eval(request.form.get('car_list'))
    total = int(request.form.get('total'))
    date = datetime.now().replace(microsecond=0)

    id_order = mdls.add_order_to_db(id_user, total, date)
    for car in car_list:
        mdls.add_car_in_orders(id_order, car)

    mdls.delete_cart(id_user)

    car_list = []

    return render_template("cart.html", car_list=car_list, id_user=id_user)



@app.route("/delete_from_cart", methods=['POST'])
def delete_from_cart():
    global cart_local
    if request.method == 'POST':
        id_user = request.form.get('id_user')
        id_car = int(request.form.get('id_car'))

        car_list = []
        if not(id_user) or id_user == 'None':
            for i, car in enumerate(cart_local):
                if car["id_car"] == id_car:
                    cart_local.pop(i)
        else:
            mdls.delete_from_cart(id_car, id_user)
            car_list = mdls.get_car_list_in_cart(id_user)
        return render_template("cart.html", car_list=car_list, id_user=id_user)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port="8080")