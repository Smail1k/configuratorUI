import requests
from flet import *
from googletrans import Translator
from config import server_endpoint


def system(page: Page):

    def name_parameters(text: str):
        for char in text:
            if char.isupper():
                text = text[:text.index(char)] + ' ' + text[text.index(char):]
        translator = Translator()
        translation = translator.translate(text, dest='ru')
        return translation.text

    data_system = requests.get(server_endpoint + "/system", headers={'Content-Type': 'application/json'}).json()

    content = Container(
        content=Column(
            controls=list(
                Container(
                    content=Row(
                        controls=[
                            Text(value=name_parameters(parameter[0]).capitalize(), size=17, weight=FontWeight.BOLD),
                            Text(value=parameter[1], size=17)
                        ],
                        expand_loose=True,
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=10,
                    border_radius=5,
                    border=border.all(width=1),
                    margin=margin.only(bottom=50) if (count == 0 or count == 4) else None
                ) for count, parameter in enumerate(data_system.items())
            ),
            scroll=ScrollMode.AUTO
        ),
        padding=10,
        expand=True
    )

    return [content]
