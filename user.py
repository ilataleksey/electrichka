from flask import Flask, render_template, request, redirect
import models as mdls


def login():
    user_phone = request.form.get('user_phone')
    user_password = request.form.get('user_password')
    users = mdls.get_users_from_db()
    for user in users:
        if user["user_phone"] == user_phone:
            if user["user_password"] == user_password:
                id_user = user["id_user"]
                user_name = user["user_name"]
                return id_user, user_name
    return None, None

def signin():
    user_phone = request.form.get('user_phone')
    user_name = request.form.get('user_name')
    user_password = request.form.get('user_password')

    id_user = mdls.add_user(user_phone, user_name, user_password)

    return id_user, user_name


# def check_password():
#     password_level = 0
#     while password_level <= 4:
#         isLong, isUp, isLow, isDig, isSpec = 0, 0, 0, 0, 0
#         text = f"Требования по улучшению пароля:\n"
#
#         user_password = input(f"Введите пароль пользователя:\n")
#
#         if re.search(r'.{8,}', user_password):
#             isLong = 1
#         else:
#             text += f"-пароль должен содержать не менее 8 символов\n"
#         if re.search(r'[A-Z]', user_password):
#             isUp = 1
#         else:
#             text += f"-пароль должен включать буквы верхнего регистра\n"
#         if re.search(r'[a-z]', user_password):
#             isLow = 1
#         else:
#             text += f"-пароль должен включать буквы нижнего регистра\n"
#         if re.search(r'[0-9]', user_password):
#             isDig = 1
#         else:
#             text += f"-пароль должен включать цифры\n"
#         if re.search(r'[@$!%*#?&£]', user_password):
#             isSpec = 1
#         else:
#             text += f"-пароль должен включать хотя бы один специальный символ: @$!%*#?&£\n"
#
#         password_level = isLong + isUp + isLow + isDig + isSpec
#
#         if password_level <= 2:
#             print("Слабый пароль - попробуйте еще раз")
#             print(text)
#             continue
#         elif password_level <= 4:
#             print("Рекомендуется улучшить пароль")
#             print(text)
#             if input("Хотите повторить попытку? y|n") != "y":
#                 break
#
#     return user_password
#
#
# def add_user():
#     print("-"*50)
#     print("Добавляем пользователя...")
#
#     exist_users = get_users_from_file()
#     if not exist_users: print("Файл для записи не найден - будет создан новый файл...")
#
#     # Вводим нового пользователя
#     is_user_exist = True
#     while is_user_exist:
#         is_user_exist = False
#         user_name = input(f"Введите имя пользователя:\n")
#
#         # Проверяем, что пользователя нет в списке
#         for user in exist_users:
#             if user_name == user["user_name"]:
#                 print("Ошибка: пользователь уже есть в списке")
#                 print("Попробуйте ввести другое имя пользователя...")
#                 is_user_exist = True
#
#     # Вводим и проверяем пароль
#     user_password = check_password()
#
#     # Создаем словарь для заполнения файла
#     user = {
#         "user_name": user_name,
#         "password": user_password,
#     }
#     users = [user]
#     is_file_exist = True
#     if not exist_users:
#         is_file_exist = False
#     write_lines_in_file(users, is_file_exist, "a")
#     print("Пользователь успешно добавлен в файл")
#     input("Нажми Enter, чтобы продолжить")
#     print("-" * 50)
#
#
# def change_password():
#     print("-" * 50)
#     print("Меняем пароль...")
#     exist_users = get_users_from_file()
#     if not exist_users:
#         print("Файл с записями не найден. Сначала добавьте хотя бы одного пользователя в файл")
#         return
#
#     user_name = input(f"Введите имя пользователя:\n")
#
#     # Проверяем, что пользователя нет в списке
#     is_user_exist = False
#     for i, user in enumerate(exist_users):
#         if user_name == user["user_name"]:
#             is_user_exist = True
#             break
#     if not is_user_exist:
#         print("Ошибка: пользователь не найден в списке")
#         print("Попробуйте еще раз или выберите добавить пользователя в меню")
#         input("Нажми Enter, чтобы продолжить")
#         print("-" * 50)
#         return
#
#     # Вводим и проверяем пароль
#     user_password = check_password()
#
#     user = {
#         "user_name": user_name,
#         "password": user_password,
#     }
#
#     exist_users[i] = user
#     is_file_exist = False
#     write_lines_in_file(exist_users, is_file_exist, "w")
#     print("Пароль успешно изменен")
#     input("Нажми Enter, чтобы продолжить")
#     print("-" * 50)