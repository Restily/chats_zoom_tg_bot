import sqlite3

from config import DATABASE_URL

def get_chats():
    connection = sqlite3.connect(DATABASE_URL)
    cursor = connection.cursor()

    try:
        cursor.execute("""
                        select *
                        from chats
                        """)

        chats = cursor.fetchall()

    except Exception as error:
        print(error)

        return None

    cursor.close()
    connection.close()

    return chats

print(get_chats())