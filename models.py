import pymysql


def get_db_connection():
    connect = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="rootmysql",
        db="softline",
        cursorclass=pymysql.cursors.DictCursor  # чтобы данные из таблицы были получены в виде списка словарей
    )
    return connect


def get_cars_from_db():
    connect = get_db_connection()
    with connect.cursor() as cursor:  # с помощью объекта cursor можно запускать sql запросы
        cursor.execute("select * from cars;")
        car_list = cursor.fetchall()  # это список словарей
    connect.close()
    return car_list


def get_car_by_id_from_db(id_car):
    connect = get_db_connection()
    with connect.cursor() as cursor:  # с помощью объекта cursor можно запускать sql запросы
        sql = "select * from cars where id=%s;"
        val = (id_car)
        cursor.execute(sql, val)
        car = cursor.fetchone()  # это словарь
    connect.close()
    return car


def get_users_from_db():
    connect = get_db_connection()
    with connect.cursor() as cursor:  # с помощью объекта cursor можно запускать sql запросы
        cursor.execute("select * from users;")
        user_list = cursor.fetchall()  # это список словарей
    connect.close()
    return user_list


def get_user_cart_id(id_user):
    connect = get_db_connection()
    with connect.cursor() as cursor:  # с помощью объекта cursor можно запускать sql запросы
        sql = f"SELECT id_cart FROM cart WHERE id_user=%s;"
        val = (id_user)
        cursor.execute(sql, val)
        id_cart = cursor.fetchone()["id_cart"]  # это словарь
        cursor.close()
    connect.close()
    return id_cart


def get_cars_in_cart(id_cart):
    connect = get_db_connection()
    with connect.cursor() as cursor:  # с помощью объекта cursor можно запускать sql запросы
        sql = f"SELECT * FROM cart_car WHERE id_cart = %s;"
        val = (id_cart)
        cursor.execute(sql, val)
        cars_in_cart = cursor.fetchall()  # это список словарей
        cursor.close()
    connect.close()
    return cars_in_cart


def get_car_list_in_cart(id_user):
    id_cart = get_user_cart_id(id_user)
    cars_in_cart = get_cars_in_cart(id_cart)
    car_list = []
    connect = get_db_connection()
    with connect.cursor() as cursor:  # с помощью объекта cursor можно запускать sql запросы
        for i, car in enumerate(cars_in_cart):
            sql = f"SELECT * FROM cars WHERE id = %s;"
            val = (car["id_car"])
            cursor.execute(sql, val)
            car_item = cursor.fetchone()  # это словарь
            car_list.append(car_item)
            car_list[i]["car_count"] = car["car_count"]
    connect.close()
    return car_list


def change_price(id, new_price):
    connect = get_db_connection()
    with connect.cursor() as cursor:
        sql = f"UPDATE cars SET price = %s WHERE id = %s;"
        val = (new_price, id)
        cursor.execute(sql, val)
        print("Price has been updated")
        connect.commit()
        print("update has been commited")
    connect.close()


def delete_car(id):
    connect = get_db_connection()
    with connect.cursor() as cursor:
        sql = f"DELETE FROM cars WHERE id = %s;"
        val = (id)
        cursor.execute(sql, val)
        print("Data has been deleted")
        connect.commit()
        print("delete has been commited")
    connect.close()


def create_table():
    connect = get_db_connection()
    with connect.cursor() as cursor:
        sql = "CREATE TABLE cars (id int AUTO_INCREMENT," \
             " title varchar(45)," \
             " price varchar(45)," \
             " img varchar(45), PRIMARY KEY (id));"
        cursor.execute(sql)
        print("Table created successfully")
    connect.close()


def insert_data():
    car_list = [] # список должен содержать словари элементов для добавления в таблицу в БД
    connect = get_db_connection()
    with connect.cursor() as cursor:
        for car in car_list:
            sql = f"INSERT INTO cars (title, price, img) VALUES (%s, %s, %s);"
            val = (car["title"], car["price"], car["img"])
            cursor.execute(sql, val)
        print("Data has been added")
        connect.commit()
        print("update has been commited")
    connect.close()


def get_car_count_in_cart(id_car, id_cart):
    connect = get_db_connection()
    with connect.cursor() as cursor:
        sql = f"SELECT car_count FROM cart_car WHERE id_car = %s AND id_cart = %s;"
        val = (id_car, id_cart)
        cursor.execute(sql, val)
        car_count = cursor.fetchone()["car_count"]  # это словарь
    connect.close()
    return car_count


def add_car_in_cart(id_car, id_user, car_count=1):
    connect = get_db_connection()
    with connect.cursor() as cursor:
        id_cart = get_user_cart_id(id_user)
        cars = get_cars_in_cart(id_cart)
        id_cars = []
        for car in cars:
            id_cars.append(car["id_car"])
        if id_car in id_cars:
            car_count_old = get_car_count_in_cart(id_car, id_cart)
            sql = f"UPDATE cart_car SET car_count = %s WHERE id_car = %s AND id_cart = %s;"
            val = (car_count_old + car_count, id_car, id_cart)
        else:
            sql = f"INSERT INTO cart_car (id_cart, id_car, car_count) VALUES (%s, %s, %s);"
            val = (id_cart, id_car, car_count)

        cursor.execute(sql, val)
        print("Car is added to cart")
        connect.commit()
        print("update has been commited")
    connect.close()


def delete_from_cart(id_car, id_user):
    connect = get_db_connection()
    id_cart = get_user_cart_id(id_user)
    with connect.cursor() as cursor:
        sql = f"DELETE FROM cart_car WHERE id_car = %s AND id_cart = %s;"
        val = (id_car, id_cart)
        cursor.execute(sql, val)
        print("Data has been deleted")
        connect.commit()
        print("delete has been commited")
    connect.close()


def get_user_id(user_phone):
    connect = get_db_connection()
    with connect.cursor() as cursor:
        sql = f"SELECT id_user FROM users WHERE user_phone = %s;"
        val = (user_phone)
        cursor.execute(sql, val)
        id_user = cursor.fetchone()["id_user"]  # это словарь
        print("Data has been received")
    connect.close()

    return id_user


def add_user(user_phone, user_name, user_password):
    connect = get_db_connection()
    with connect.cursor() as cursor:
        sql = f"INSERT INTO users (user_name, user_phone, user_password) VALUES (%s, %s, %s);"
        val = (user_name, user_phone, user_password)
        cursor.execute(sql, val)
        connect.commit()

        id_user = get_user_id(user_phone)
        sql = f"INSERT INTO cart (id_user) VALUES (%s);"
        val = (id_user)

        cursor.execute(sql, val)
        print("User is added to db")
        connect.commit()
        print("update has been commited")
    connect.close()

    return id_user


def add_order_to_db(id_user, total, date):
    connect = get_db_connection()
    with connect.cursor() as cursor:
        sql = f"INSERT INTO orders (id_user, date, total) VALUES (%s, %s, %s);"
        val = (id_user, date, total)
        cursor.execute(sql, val)
        connect.commit()

        sql = f"SELECT id_order FROM orders WHERE id_user = %s AND date = %s AND total = %s;"
        val = (id_user, date, total)
        cursor.execute(sql, val)
        id_order = cursor.fetchone()["id_order"]  # это словарь
    connect.close()

    return id_order


def add_car_in_orders(id_order, car):
    connect = get_db_connection()
    with connect.cursor() as cursor:
        sql = f"INSERT INTO order_cars (id_order, id_car, car_count) VALUES (%s, %s, %s);"
        val = (id_order, int(car["id"]), car["car_count"])
        cursor.execute(sql, val)
        connect.commit()
    connect.close()


def delete_cart(id_user):
    connect = get_db_connection()
    cart_id = get_user_cart_id(id_user)
    with connect.cursor() as cursor:
        sql = f"DELETE FROM cart_car WHERE id_cart = %s;"
        val = (cart_id)
        cursor.execute(sql, val)
        print("Data has been deleted")
        connect.commit()
        print("delete has been commited")
    connect.close()
    return None