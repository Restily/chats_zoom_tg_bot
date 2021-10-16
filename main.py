from utils import create_zoom_meet
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN, ADMIN_ID
from keyboard import default_buttons, Keyboard


bot = Bot(token=API_TOKEN)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)

keyboards = {}

class States(StatesGroup):
    student = State()
    months = State()
    days = State()
    time = State()
    complete = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Здравствуйте! Чтобы создать конференцию, нажмите на кнопку ниже',
                            reply_markup=default_buttons)


@dp.message_handler(lambda message: message.text == 'Создать конференцию💻', state='*')
async def create_conference(message: types.Message, state: FSMContext=None):

    if state:
        await state.finish()
    
    try:
        user_id = message.from_user.id
        
        keyboards[user_id] = Keyboard(teacher_id=user_id)

        students_buttons = keyboards[user_id].get_students_buttons()

        if not students_buttons:
            await bot.send_message(chat_id=user_id, text='Доступ запрещен')

            return None

        await bot.send_message(chat_id=user_id, text='Выберите ученика:', 
                                reply_markup=students_buttons)

        await States.student.set()

    except Exception as error:
        print(error)


@dp.callback_query_handler(state=States.student)
async def select_student(call: CallbackQuery, state: FSMContext):
    try:
        user_id = call.from_user.id

        keyboards[user_id].get_student(call.data)

        await bot.edit_message_reply_markup(chat_id=user_id, 
                                            message_id=call.message.message_id, reply_markup=None)

        await bot.send_message(chat_id=user_id, 
                                text='\tВыберите дату:\t', 
                                reply_markup=keyboards[user_id].get_months_buttons())

        await state.finish()
        await States.months.set()

    except Exception as error:
        print(error)


@dp.callback_query_handler(state=States.months)
async def select_student(call: CallbackQuery, state: FSMContext):
    try:
        user_id = call.from_user.id

        keyboards[user_id].set_month(call.data)

        await bot.edit_message_reply_markup(chat_id=user_id, 
                                            message_id=call.message.message_id, 
                                            reply_markup=keyboards[user_id].get_days_buttons())

        await state.finish()
        await States.days.set()

    except Exception as error:
        print(error)


@dp.callback_query_handler(state=States.days)
async def select_student(call: CallbackQuery, state: FSMContext):
    try:
        user_id = call.from_user.id

        keyboards[user_id].set_day(call.data)

        await bot.edit_message_reply_markup(chat_id=user_id, 
                                            message_id=call.message.message_id, 
                                            reply_markup=None)

        await bot.send_message(chat_id=user_id, text='Введите и отправьте время в формате "часы:минуты", например 14:00')

        await state.finish()
        await States.complete.set()

    except Exception as error:
        print(error)


@dp.message_handler(state=States.complete)
async def complete_zoom(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    kb = keyboards[user_id]

    kb.set_time(message.text)

    zoom_message = create_zoom_meet(kb)

    if zoom_message == None:
        await bot.send_message(chat_id=user_id, text='Произошла ошибка. Попробуйте создать конферецию заново')
    else:
        await bot.send_message(chat_id=user_id, text=zoom_message)
        await bot.send_message(chat_id=ADMIN_ID, text='Репетитор @{} ({}) создал встречу с учеником :\n\n{}'.format(
            message.from_user.username,
            kb.teacher_name,
            zoom_message
        ))  

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)