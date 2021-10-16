import sqlite3

from config import DATABASE_URL

def get_teacher_students(teacher_id):
    connection = sqlite3.connect(DATABASE_URL)
    cursor = connection.cursor()

    try:
        cursor.execute("""
                        select student_id, student_name
                        from chats
                        where teacher_id = {}
                        """.format(teacher_id))

        students = cursor.fetchall()

    except Exception as error:
        print(error)

        return None

    cursor.close()
    connection.close()

    return students


def get_teacher_name(teacher_id):
    connection = sqlite3.connect(DATABASE_URL)
    cursor = connection.cursor()

    try:
        cursor.execute("""
                        select teacher_name
                        from chats
                        where teacher_id = {}
                        """.format(teacher_id))

        teacher_name = cursor.fetchone()[0]

    except Exception as error:
        print(error)

        return None

    cursor.close()
    connection.close()

    return teacher_name

# def insert_chat_to_database(Chat: object) -> bool:
#     connection = sqlite3.connect(DATABASE_URL)
#     cursor = connection.cursor()
    
#     try:
#         cursor.execute("""
#                         insert into chats (chat_id, teacher_id, teacher_nick, teacher_name, student_id, student_nick, student_name) 
#                         values (?, ?, ?, ?, ?, ?, ?)
#                         """, (
#                             Chat.chat_id,
#                             Chat.teacher_id,
#                             Chat.teacher_nick,
#                             Chat.teacher_name,
#                             Chat.student_id,
#                             Chat.student_nick,
#                             Chat.student_name
#         ))
#         connection.commit()

#     except Exception as error:
#         print(error)

#     cursor.close()
#     connection.close()


# class Chat:
#     chat_id = 11242123
#     teacher_id = 588455220
#     teacher_nick = '@aidreika'
#     teacher_name = 'Андрей'
#     student_id = 582475909
#     student_nick = '@Restily'
#     student_name = 'Тимур'

# chat = Chat

# insert_chat_to_database(chat)