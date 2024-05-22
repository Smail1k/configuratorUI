import requests
from flet import *
from time import sleep

import config
from config import server_endpoint


def authorization(page: Page):
    def enter(e: ContainerTapEvent):
        if not login_auth.value:
            login_auth.error_text = "Пожалуйста, введите свой логин"
            if isinstance(page.views[0].controls[0].controls[3], text.Text):
                page.views[0].controls[0].controls.pop(3)
            page.update()
            return
        else:
            login_auth.error_text = None

        if not password_auth.value:
            password_auth.error_text = "Пожалуйста, введите свой пароль"
            page.update()
            return
        else:
            password_auth.error_text = None

        page.go("/quick")
        # response = requests.post(url=server_endpoint + "/authorization",
        #                          data={'username': login_auth.value,
        #                                'password': password_auth.value})
        # if response.status_code == 200:
        #     dlg = AlertDialog(title=Text(value="Успешно", color=colors.GREEN), content=Text(
        #         value="С возвращением!", text_align=TextAlign.LEFT, size=30))
        #     page.dialog = dlg
        #     dlg.open = True
        #     page.update()
        #     sleep(1)
        #     dlg.open = False
        #     config.token = response.json()['access_token']
        #     page.go("/quick")
        # else:
        #     error_txt = Text(value="Неправильный логин или пароль",
        #                      color=colors.ERROR, text_align=TextAlign.CENTER)
        #     if isinstance(page.views[1].controls[0].controls[3], text.Text):
        #         return
        #     else:
        #         page.views[1].controls[0].controls.insert(3, error_txt)
        #         page.update()

    page.clean()

    txt_auth = Text(value="Авторизация", size=25, text_align=TextAlign.CENTER)
    login_auth = TextField(label="Имя пользователя", width=250, border_radius=8)
    password_auth = TextField(label="Пароль", width=250
                              , border_radius=8, password=True, can_reveal_password=True)
    come_in_auth = TextButton(content=Text(value="Войти", size=20, text_align=TextAlign.CENTER), on_click=enter)

    authorization_column = Column(
        controls=[txt_auth, login_auth, password_auth, come_in_auth],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=20
    )

    return authorization_column
