import json

import requests
from flet import *
from googletrans import Translator

from config import server_endpoint
from src.resources.translation_dictionary import translations


def openssh(page: Page):
    # def name_parameters(text: str):
    #     for char in text:
    #         if char.isupper():
    #             text = text[:text.index(char)] + ' ' + text[text.index(char):]
    #     translator = Translator()
    #     translation = translator.translate(text, dest='ru')
    #     return translation.text

    def on_parameter_change(e):
        data_update = {'parameterName': e.control.data, 'parameterValue': e.control.value}
        data_update_json = json.dumps(data_update)
        requests.patch(server_endpoint + "/ssh", headers={'Content-Type': 'application/json'},
                       data=data_update_json)

    response = requests.get(server_endpoint + "/ssh", headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        data_ssh = response.json()

    content = Container(
        content=Column(
            controls=list(
                Container(
                    content=Row(
                        controls=[
                            Text(value=translations['russian'][parameter[0].lower()], size=17, weight=FontWeight.BOLD,
                                 max_lines=2, overflow="ellipsis", width=400),
                            Switch(value=parameter[1], on_change=on_parameter_change, data=parameter[0]) if parameter[1]
                            in [True, False] else TextField(value=parameter[1], width=550, text_size=17,
                                                            bgcolor="#ebebeb", data=parameter[0],
                                                            on_submit=on_parameter_change)
                        ],
                        expand_loose=True,
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=10,
                    border_radius=5,
                    border=border.all(width=1)
                ) for parameter in data_ssh.items()
            ),
            scroll=ScrollMode.AUTO
        ),
        padding=10,
        expand=True
    )

    return [content]
