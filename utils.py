import jwt
import requests
import json
from time import time

from keyboard import Keyboard
from config import API_KEY, API_SEC


def generateToken():
    try:
        token = jwt.encode(
            {'iss': API_KEY, 'exp': time() + 5000},
            API_SEC,
            algorithm='HS256'
        ).decode('UTF-8')

        return token
        
    except Exception as error:
        print(error)


def create_zoom_meet(kb):
    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}

    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings', 
        headers=headers, data=json.dumps(
                                    {"topic": "Конференция",
                                    "type": 2,
                                    "start_time": "{}-{}-{}T{}:00".format(
                                        kb.year,
                                        kb.month,
                                        kb.day,
                                        kb.time
                                    ),
                                    "duration": "135",
                                    "timezone": "Europe/Moscow",
                    
                                    "recurrence": {"type": 1,
                                                    "repeat_interval": 1
                                                    },

                                    "settings": {"host_video": "false",
                                                "participant_video": "false",
                                                "join_before_host": "true",
                                                "mute_upon_entry": "False",
                                                "watermark": "true",
                                                "audio": "voip",
                                                "auto_recording": "cloud"
                                                }
                                    }))
        
    try:
        meet = json.loads(r.text)

        join_URL = meet["join_url"]
        meetingPassword = meet["password"]

        months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 
                    'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

        date = '{} {} {} в {}'.format(
            kb.day,
            months[kb.month - 1],
            kb.year,
            kb.time
        )

        return f'Конференция пройдет {date}\nСсылка на конференцию:{join_URL}\nПароль:{meetingPassword}'
    
    except Exception as error:
        print(error)
    
        return None