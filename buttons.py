
import sqlite3


cnn = sqlite3.connect("base.db")
cur = cnn.cursor()

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import *



async def back_btn_FUNC(btn_markup):

    back_buttons = {
        "📝Kursga yozilish" : "kursgaYozilish",
        "◀️Ortga" : "main_back"
    }

    for key, value in back_buttons.items():
        btn_markup.add(InlineKeyboardButton(text = key, callback_data = value))

    return btn_markup

mainButtonsDict = { # Основные кнопки

    "🏢O'quv marakz" : "oquvMarkaz",
    "🗂Bizning kurslar" : "bizningKurslar",
    "📞Biz bilan bog'lanish" : "bizBB",
    "📝Kursga yozilish" : "kursgaYozilish"

    }

async def main_menu_btn_generation():

    btn = InlineKeyboardMarkup(row_width = 2)

    for key, value in mainButtonsDict.items():
        btn.insert(InlineKeyboardButton(text = key, callback_data = value))

    return btn


cur.execute("select * from courses")
courses = cur.fetchall()

async def show_Courses():

    btn = InlineKeyboardMarkup()

    for i in range(len(courses)):
        btn.add(InlineKeyboardButton(text = courses[i][-1], callback_data = courses[i][-2]))

    await back_btn_FUNC(btn)

    return btn
    

async def coursePen(data):
    btn = InlineKeyboardMarkup()

    back_buttons = {
        "📝Kursga yozilish" : f"course_{data}",
        "◀️Ortga" : f"corses_back"
    }

    for key, value in back_buttons.items():

        btn.add(InlineKeyboardButton(text = key, callback_data = value))

    return btn

    

mainButtonsCaption = { # callback_data -ы основного меню ⬆️

    "oquvMarkaz" : "Bizning fillialarimiz!",
    "bizningKurslar" : "Bizning kurslar",
    "bizBB" : "Qo'shimcha savol va takliflar uchun\ntel: +998981219808",
    "kursgaYozilish" : "FUNC"

}


async def gn_checkInfoButtons():

    choose = {
        "Xa✅" : "yes",
        "Yo'q❌" : "no"
        }
    
    checkInfoButtons = InlineKeyboardMarkup(row_width = 2)
    
    for key, value in choose.items():
        checkInfoButtons.insert(InlineKeyboardButton(text = key, callback_data = value))

    return checkInfoButtons


async def location_generate():

    cur.execute("select * from location")
    location = cur.fetchall()
    
    btn = InlineKeyboardMarkup()

    for i in range(len(location)):
        btn.add(InlineKeyboardButton(text = location[i][0], callback_data = location[i][-1]))

    btn.add(InlineKeyboardButton(text = "◀️Ortga", callback_data = "main_back"))

    return btn



async def courseKB():
    cur.execute("select * from courses")
    coursesI = cur.fetchall()

    btn = ReplyKeyboardMarkup()

    for i in coursesI:
        btn.add(KeyboardButton(text = i[-1]))

    return btn








#####################################   ADMIN  #####################################

admin_panel_inline_btn = {

    "Kurslar" : "courses_in_admin_panel",
    "E'lon berish" : "announcement"

}

courses_create_list = ["Kursni o'zgartirish 📝", "Kursni o'chirish 🗑", "Kurs qo'shish ➕"]


async def admin_btn():

    btn = InlineKeyboardMarkup()

    for key, value in admin_panel_inline_btn.items():
        btn.insert(InlineKeyboardButton(text = key, callback_data = value))

    return btn



async def add_course_in_admin():

    btn = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)

    for i in courses_create_list:
        btn.insert(KeyboardButton(text = i))

    return btn



coursesList = []


async def show_Courses_in_admin():

    btn = ReplyKeyboardMarkup()

    for i in range(len(courses)):
        coursesList.append(courses[i][-1])
        btn.add(KeyboardButton(text = courses[i][-1]))

    return btn




admin_panel_function = ["Kurs nomini 📝", "Kurs vaqtini ⏰", "Kursning davomiyligini ⏰", "Kurs xaqidagi ma'lumotlarni ℹ️", "Kurs narxini 💰", "Kurs rasmini 🖼"]


async def courses_create_in_admin_p():

    btn = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)

    for i in admin_panel_function:
        btn.insert(KeyboardButton(text = i))

    return btn