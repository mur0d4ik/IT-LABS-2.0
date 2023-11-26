import re
import sqlite3



cnn = sqlite3.connect("base.db")
cur = cnn.cursor()

async def createTables():

    cur.execute("""create table if not exists user(
                id integer,
                username varchar(150)
    )""")


async def createUserCourses():

    cur.execute("""create table if not exists userCourses(
                name varchar(100),
                time varchar(6),
                duration_time varchar(3),
                duration varchar(3),
                description text
    )""")


async def createLocationTables(): # Создаю таблицу в которой находится широта и долгота проще местополежения

    cur.execute("""create table if not exists location(
                name text,
                X text,
                Y text,
                calldata text
    )""")


async def createInfoInCoursesTables(): # Создаю таблицу в которой находится широта и долгота проще местополежения

    cur.execute("""create table if not exists courses(
                img text,
                caption text
    )""")


    

async def select_user(idS):
    cur.execute("select * from user where id = {}".format(idS))
    return cur.fetchone()


async def add_user(idA, username):

    selectUser = await select_user(idA)

    if selectUser:
        return False

    else:
        cur.execute("""insert into user values('{}','{}')""".format(idA,username))
        cnn.commit()

        print(f"id -> {idA}\nusername -> {username}")


async def selectUserCourse(data):
    cur.execute("select * from courses")
    coursesI = cur.fetchall()

    _ = data.index("_")
    course_name = ""

    for i in coursesI:
        if str(data[_ + 1:]) in i[-2]:
            course_name = i[-1]

    return course_name


location_list = []

def search_location():

    cur.execute("select * from location")
    location = cur.fetchall()

    for i in range(len(location)):
        location_list.append(location[i][-1])


