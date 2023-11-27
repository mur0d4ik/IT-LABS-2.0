import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from buttons import *
from config import *
from state import *
from baseFunc import *

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
state = FSMContext

 
# @dp.message_handler(content_types = "photo")
# async def af(message: types.Message):
#     await message.answer(message.photo[-1].file_id)
 
# Основная фотография -> AgACAgIAAxkBAAM7ZWBKxvYS8bye2UJ-78pTMHtomOoAAvjSMRu_ygABS_niOc8bJrchAQADAgADeQADMwQ

cur.execute("select * from courses")
coursesI = cur.fetchall()

cur.execute("select * from location")
location = cur.fetchall()

createUserCourses()

@dp.message_handler(commands = "start")
async def welCome(message: types.Message):
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer("Asosiy menu: ", reply_markup = await main_menu_btn_generation())



@dp.message_handler(commands = "admin")
async def welCome(message: types.Message):

    if message.from_user.id == admin or message.from_user.id == 6036442860:
        await message.answer("Xush kelibsiz admin!", reply_markup = await admin_btn())

    else:
        await message.answer("Siz admin emassiz!!!")


cur.execute("select * from courses")
coursesFULL = cur.fetchall()

# print(*coursesFULL[1])
@dp.callback_query_handler()
async def cal(call: types.CallbackQuery):

    search_location()

    #   Админ панель...
    if call.data == "courses_in_admin_panel":
        await call.message.answer("Kurs(lar) bilan nima qilmoqchisiz?", reply_markup = await add_course_in_admin())


    if call.data == "bizningKurslar":
        await call.message.answer_photo(
            photo = "AgACAgIAAxkBAAM7ZWBKxvYS8bye2UJ-78pTMHtomOoAAvjSMRu_ygABS_niOc8bJrchAQADAgADeQADMwQ",
            caption = mainButtonsCaption[call.data], reply_markup = await show_Courses()
            )
        
    #   Это часть кода для вывода курсов (фотография, описания, кнопки)
    elif call.data not in mainButtonsCaption.keys() and call.data[-4:] != "back":
        for i in range(len(courses)):
            if call.data == courses[i][-2]:
                await call.message.answer_photo(
                    photo = f"{courses[i][0]}",
                    caption = f"{courses[i][1]}", reply_markup = await coursePen(courses[i][-2])
                )


    elif call.data == "bizBB":
        await call.message.answer(mainButtonsCaption[call.data], reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "◀️Ortga", callback_data = "main_back")))
                
    #    Это часть оператора проверяет все кнопки " back "
    if call.data[-4:] == "back":


        if call.data == "main_back":
            await call.message.answer("Asosiy menu: ", reply_markup = await main_menu_btn_generation())


        elif call.data == "corses_back":
            await call.message.answer_photo(
            photo = "AgACAgIAAxkBAAM7ZWBKxvYS8bye2UJ-78pTMHtomOoAAvjSMRu_ygABS_niOc8bJrchAQADAgADeQADMwQ",
            caption = mainButtonsCaption["bizningKurslar"], reply_markup = await show_Courses()
            )

        elif call.data == "location_back":
            await call.message.answer_photo(
            photo = "AgACAgIAAxkBAAM7ZWBKxvYS8bye2UJ-78pTMHtomOoAAvjSMRu_ygABS_niOc8bJrchAQADAgADeQADMwQ",
            caption = mainButtonsCaption["oquvMarkaz"], reply_markup = await location_generate()
            )

    #   Это часть для вывода меня всех филлиалов
    elif call.data == "oquvMarkaz":
        await call.message.answer_photo(
            photo = "AgACAgIAAxkBAAM7ZWBKxvYS8bye2UJ-78pTMHtomOoAAvjSMRu_ygABS_niOc8bJrchAQADAgADeQADMwQ",
            caption = mainButtonsCaption[call.data], reply_markup = await location_generate()
            )

    # Это часть кода для вывода геолокации(местоположении)
    elif call.data in location_list:
        location_index = location_list.index(call.data)
        await bot.send_location(call.from_user.id, location[location_index][1], location[location_index][2], reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "◀️Ortga", callback_data = "location_back")))


    elif call.data == "kursgaYozilish":

        await call.message.answer("✍️ <b>To'liq ismingizni kiriting</b>", parse_mode = "HTML")
        await cours.name.set()


        @dp.message_handler(state = cours.name)
        async def nameUser(message: types.Message, state: FSMContext):
            await state.update_data(name = message.text)

            await message.answer("📧 <b>Yoshingizni kiriting</b>", parse_mode = "HTML")
            await cours.age.set()


        @dp.message_handler(state = cours.age)
        async def ageUser(message: types.Message, state: FSMContext):
            if message.text.isdigit():
                await state.update_data(age = message.text)

                await message.answer("Kursni tanglang: ", reply_markup = await courseKB())
                await cours.courses.set()


            else:
                await message.answer("❌Yoshingizni sonlarda kiriting!")

        @dp.message_handler(state = cours.courses)
        async def chooseCourse(message: types.Message, state: FSMContext):
            await state.update_data(courses = message.text)

            await message.answer("📞 Telefon nomeringizni yuboring!", reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton(text = "📞 Telefon nomer",request_contact = True)))
            await cours.phone_number.set()

        @dp.message_handler(content_types = "contact", state = cours.phone_number)
        async def phoneNumberUser(message: types.Message, state: FSMContext):
            await state.update_data(phone_number = message.contact["phone_number"])

            data = await state.get_data()
            name = data.get("name")
            age = data.get("age")
            cours_ = data.get("courses")
            phone_number = data.get("phone_number")

            info = f"""☑️ Sizning ma'lumotlaringiz

📄 F.I.O: - {name}
👤 Yosh: {age}
🖥 Kurs: {cours_}
📞 Telefon: {phone_number}

⚠️ Ma'lumotlaringiz to'g'rimi?"""
            

            await message.answer(info, reply_markup = await gn_checkInfoButtons())
            await cours.check.set()

        @dp.callback_query_handler(state = cours.check)
        async def checkChoose(call: types.CallbackQuery,state: FSMContext):
            
            data = await state.get_data()
            name = data.get("name")
            age = data.get("age")
            courses = data.get("courses")
            phone_number = data.get("phone_number")

            info = f"""✅Qabul qilingan ma'lumotar!

📄 F.I.O: - {name}
🌀 Username: @{call.from_user.username}
👤 Yosh: {age}
🖥 Kurs: {courses}
📞 Telefon: {phone_number}"""
            
            if call.data == "yes":
                await bot.send_message(chat_id = admin, text = info)
                await call.message.answer("Malumotlaringiz adminga yuborildi✅", reply_markup = types.ReplyKeyboardRemove())

            else:
                await call.message.answer("Ma'lumotlaringiz o'chirildi🔥")


            await state.finish()
            await state.reset_state()

    #    Это часть кода автономна , она автоматически узнает какой курс вы выбрали
    elif call.data[:7] == "course_":


        await call.message.answer("✍️ <b>To'liq ismingizni kiriting</b>", parse_mode = "HTML")
        await cours.name.set()


        @dp.message_handler(state = cours.name)
        async def nameUser(message: types.Message, state: FSMContext):
            await state.update_data(name = message.text)

            await message.answer("📧 <b>Yoshingizni kiriting</b>", parse_mode = "HTML")
            await cours.age.set()


        @dp.message_handler(state = cours.age)
        async def ageUser(message: types.Message, state: FSMContext):
            if message.text.isdigit():
                await state.update_data(age = message.text)

                await message.answer("📞 <b>Telefon raqam yuboring</b>", reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton(text = "📞 Telefon raqam",request_contact = True)),parse_mode = "HTML")
                await cours.phone_number.set()


            else:
                await message.answer("❌Yoshingizni sonlarda kiriting!")


        @dp.message_handler(content_types = "contact", state = cours.phone_number)
        async def phoneNumberUser(message: types.Message, state: FSMContext):
            await state.update_data(phone_number = message.contact["phone_number"])

            global course_ 
            course_ = await selectUserCourse(call.data)

            data = await state.get_data()
            name = data.get("name")
            age = data.get("age")
            phone_number = data.get("phone_number")

            info = f"""☑️ Sizning ma'lumotlaringiz

📄 F.I.O: - {name}
👤 Yosh: {age}
🖥 Kurs: {await selectUserCourse(call.data)}
📞 Telefon: {phone_number}

⚠️ Ma'lumotlaringiz to'g'rimi?"""


            await call.message.answer("...",reply_markup = types.ReplyKeyboardRemove())
            await message.answer(info, reply_markup = await gn_checkInfoButtons())
            await message.delete()
            await cours.check.set()

        @dp.callback_query_handler(state = cours.check)
        async def checkChoose(call: types.CallbackQuery,state: FSMContext):
            
            data = await state.get_data()
            name = data.get("name")
            age = data.get("age")
            phone_number = data.get("phone_number")

            info = f"""✅Qabul qilingan ma'lumotar!

📄 F.I.O: - {name}
🌀 Username: @{call.from_user.username}
👤 Yosh: {age}
🖥 Kurs: {course_}
📞 Telefon: {phone_number}"""
            
        
            await state.finish()
            await state.reset_state()
            


            #   Это часть кода отправляет " Информацию " админу если call.data == "yes", а есди наоборот то код отправляет сообщения "Ma'lumotlaringiz o'chirildi🔥"
            if call.data == "yes":
                await bot.send_message(chat_id = admin, text = info)
                await call.message.answer("Malumotlaringiz adminga yuborildi✅", reply_markup = types.ReplyKeyboardRemove())

            else:
                await call.message.answer("Ma'lumotlaringiz o'chirildi🔥")
        


@dp.message_handler()
async def command_in_admin(message: types.Message):
    if message.text == "Kursni o'zgartirish 📝":
        await message.answer("Qaysi kursga o'zgartirish kiritish kerak?", reply_markup = await show_Courses_in_admin())

    elif message.text in coursesList:
        await message.answer("Kursni nimasini o'zgartirasiz?", reply_markup = await courses_create_in_admin_p())

    elif message.text == "Kurs qo'shish ➕":
        await message.answer("✍️ Kurs nomini kiriting: ", reply_markup = types.ReplyKeyboardRemove())

        await coursADD.cours_name.set()

    
    @dp.message_handler(state = coursADD.cours_name)
    async def name_of_cours(message: types.Message, state: FSMContext):

        await state.update_data(cours_name = message.text)
        await message.answer("⏰ Kurs vaqtini yozing daqiqada! ~(90): ")
        await coursADD.cours_time.set()

    
    @dp.message_handler(state = coursADD.cours_time)
    async def time_of_cours(message: types.Message, state: FSMContext):

        if message.text.isdigit():
            await state.update_data(cours_time = message.text)
            await message.answer("📅 Kursning davomiyligini yozing oyda ~(9): ")
            await coursADD.cours_duration.set()

        else:
            await message.answer("❌Dars vaqtini sonda kiriting!!!")



    @dp.message_handler(state = coursADD.cours_duration)
    async def duration_of_cours(message: types.Message, state: FSMContext):

        if message.text.isdigit():
            await state.update_data(cours_duration = message.text)
            await message.answer("ℹ️ Kurs haqida ma'lumot yozing: ")
            await coursADD.cours_discription.set()

        else:
            await message.answer("❌Kursning davomiyligini sonda yozing!")

    @dp.message_handler(state = coursADD.cours_discription)
    async def cours_discription_of_cours(message: types.Message, state: FSMContext):

        await state.update_data(cours_discription = message.text)
        await message.answer("💸 Kurs narxini kiriting so'mda!: ~(599.000)")
        await coursADD.cours_price.set()


    
    @dp.message_handler(state = coursADD.cours_price)
    async def cours_discription_of_cours(message: types.Message, state: FSMContext):

        await state.update_data(cours_price = message.text)
        await message.answer("🖼 Kursni rasmini yuboring")
        await coursADD.cours_photo.set()


    @dp.message_handler(content_types = "photo", state = coursADD.cours_photo)
    async def cours_discription_of_cours(message: types.Message, state: FSMContext):
        
        print(message.photo[-1].file_id)
        
        await state.update_data(cours_photo = message.photo[-1].file_id)

        data = await state.get_data()
        cours_name = data.get("cours_name")
        cours_time = data.get("cours_time")
        cours_duration = data.get("cours_duration")
        cours_discription = data.get("cours_discription")
        cours_price = data.get("cours_price")
        cours_photo = data.get("cours_photo")

        text = f"""{cours_name}

⏰Dars vaqti: {cours_time} daqiqa

📅 Kurs davomiyligi {cours_duration} oy

💸 Kurs narxi oyiga {cours_price} so'm.

{cours_discription}

📌 Kurs davomida shaxsiy portfolio yaratasiz.

🚀 Darslarda 100% amaliy bilimlarga ega bo'lasiz.
"""
        
        await add_createUserCourses(cours_name, cours_time, cours_duration, cours_discription, cours_price, cours_photo)
        await message.answer("✅ Kurs bazaga qo'shildi")
        
        await bot.send_photo(
            chat_id = message.from_user.id,
            photo = cours_photo,
            caption = text
            )
        
        





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)