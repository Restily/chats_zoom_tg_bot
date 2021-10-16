import time

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup 
from aiogram.utils.callback_data import CallbackData

from calendar import month, monthrange
from datetime import date, datetime
from database import get_teacher_students, get_teacher_name

cb_student = CallbackData('student_call', 'student_id', 'student_name')
cb_month = CallbackData('month_call', 'month', 'flag')
cb_day = CallbackData('day_call', 'day')

default_buttons = ReplyKeyboardMarkup([[KeyboardButton('Создать конференцию💻')]], resize_keyboard=True)


class Keyboard():

    def __init__(self, teacher_id):
        self.teacher_id = teacher_id
        self.teacher_name = ''
        self.student_id = int
        self.student_name = ''
        self.year = int
        self.month = 0
        self.day = 0
        self.time = ''


    def get_students_buttons(self):
        keyboard_students = InlineKeyboardMarkup()

        students = get_teacher_students(self.teacher_id)

        if students == []:
            return None

        for student in students:
            keyboard_students.add(InlineKeyboardButton(student[1], 
                                    callback_data=cb_student.new(student_id=student[0], student_name=student[1])))

        return keyboard_students


    # def check_time(self):
    #     cur_date = datetime.now()

    #     if self.month == cur_date.month:
    #         if self.day != 0:
    #             if self.day < cur_date.day:
    #                 return False
        
    #     if self.time != '':
    #         try:
    #             time.strptime(self.time, '%H:%M')
                
    #         except ValueError:
    #             return False


    def get_student(self, call_data):
        call_data = str(call_data).split(':')

        self.student_id = int(call_data[1])
        self.student_name = call_data[2]


    def get_months(self):
        cur_month = datetime.now().month

        if cur_month == 12:
            next_month = 1
        else:
            next_month = cur_month + 1

        return cur_month, next_month 

    
    def set_month(self, call_data):
        call_data = str(call_data).split(':')
        self.month = int(call_data[1])

        if call_data[2] == 'next' and self.month == 1:
            self.year == datetime.now().year + 1
        else:
            self.year = datetime.now().year


    def set_day(self, call_data):
        self.day = str(call_data).split(':')[1]


    def set_time(self, time):
        if len(time) == 4:
            time = '0' + time
            
        self.time = time
        

    def get_months_buttons(self):
        cur_month, next_month = self.get_months()

        months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
                    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        keyboard_months = InlineKeyboardMarkup()
        keyboard_months.add(InlineKeyboardButton(months[cur_month - 1], callback_data=cb_month.new(month=cur_month, flag='current')))
        keyboard_months.add(InlineKeyboardButton(months[next_month - 1],callback_data=cb_month.new(month=next_month, flag='next')))

        return keyboard_months
    

    def get_days_buttons(self):
        days = monthrange(self.year, self.month)[1]

        keyboard = []
        row = []

        for day in range(1, days + 1):
            row.append(InlineKeyboardButton(f'{day}', callback_data=cb_day.new(day=day)))    

            if day % 7 == 0:
                keyboard.append(row)

                row = []
                
        if row != []:
            keyboard.append(row)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def get_date(self):
        return '{}-{}-{} {}'.format(
            self.year,
            self.month,
            self.day,
            self.time
        )

# kb = Keyboard()
# kb.get_months_buttons()
# kb.get_days_buttons()