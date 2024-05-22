import json
import requests
from flet import *

import password_hashing
from config import server_endpoint
from src.resources.static_data import user_back_colors
from models.user import User


def users(page: Page):
    data_users = requests.get(server_endpoint + "/users", headers={'Content-Type': 'application/json'}).json()
    data_users = [User(**user_data) for user_data in data_users]

    def on_hover(e):
        if e.control.data == "delete" or e.control.data == "cancel":
            e.control.bgcolor = "#e60b00" if e.data == "true" else colors.RED
        else:
            e.control.bgcolor = "#19ff19" if e.data == "true" else "#16a131"
        e.control.update()

    def on_parameter_change(e):
        user = data_users[user_page_content.selected_index]
        user.__setattr__(e.control.data, e.control.value)
        user_dict = user.dict()
        user_json = json.dumps(user_dict)
        requests.patch(server_endpoint + f"/users/{user.id}", headers={'Content-Type': 'application/json'},
                       data=user_json)
        if e.control.data == "fullname":
            e.control.border_color = page.bgcolor
            e.control.border_width = 0
        elif e.control.data == "autoIn":
            for index, tab in enumerate(user_page_content.tabs):
                if index != user_page_content.selected_index:
                    user_page_content.tabs[index].content.content.controls[6].content.controls[2].trailing.value = False

        page.update()

    def on_change_password(e):
        user = data_users[user_page_content.selected_index]

        def on_change_textfield(e):
            # Проверяем, не пустые ли оба поля ввода пароля
            all_fields_filled = all(
                field.value for field in dlg.content.controls if isinstance(field, TextField)
            )

            # Включаем или отключаем кнопку "Задать пароль" в зависимости от заполненности полей
            dlg.actions[1].disabled = not all_fields_filled
            dlg.actions[1].bgcolor = "#16a131" if all_fields_filled is True else "#efefef"
            dlg.actions[1].update()  # Обновляем кнопку для отображения изменений

        def on_set_new_password(e):
            if user.password is not None:
                if not password_hashing.verify_password(dlg.content.controls[0].value, user.password):
                    dlg.content.controls[0].error_text = "Неверный пароль"
                    dlg.content.controls[0].errol_style = TextStyle(color=colors.ERROR)

            if dlg.content.controls[-2].value == dlg.content.controls[-1].value:
                user.password = dlg.content.controls[-1].value
                requests.patch(server_endpoint + f"/users/{user.id}", headers={'Content-Type': 'application/json'},
                               data=user).json()
                dlg.open = False
            else:
                dlg.content.controls[-1].error_text = "Пароли не совпадают"
                dlg.content.controls[-1].errol_style = TextStyle(color=colors.ERROR)

            page.update()

        def on_cancel(e):
            dlg.open = False
            page.update()

        dlg_content = [TextField(value=None, label="Новый пароль", data="new_password", password=True,
                                 can_reveal_password=True,
                                 helper_text="Смешайте заглавные и строчные буквы несколько раз",
                                 on_change=on_change_textfield),
                       TextField(value=None, label="Подтвердите новый пароль", data="new_password_confirmation",
                                 password=True, can_reveal_password=True, on_change=on_change_textfield)]

        if data_users[user_page_content.selected_index].password is not None:
            dlg_content.insert(0, TextField(value=None, label="Текущий пароль", data="password",
                                            password=True, can_reveal_password=True, on_change=on_change_textfield))

        dlg = AlertDialog(
            title=Row(controls=[Text(value="Изменить пароль", size=18)], alignment=MainAxisAlignment.CENTER),
            content=Column(
                controls=dlg_content, spacing=20, height=300, width=400),
            actions=list(
                Container(
                    content=Text(value=txt, size=16),
                    bgcolor="#efefef" if data == "change" else clr,
                    border=border.all(width=1, color=colors.BLACK),
                    border_radius=5,
                    padding=padding.symmetric(vertical=8, horizontal=30),
                    margin=margin.only(left=20, right=20),
                    data=data,
                    disabled=True if data == "change" else False,
                    on_hover=on_hover,
                    on_click=on_cancel if data == "cancel" else on_set_new_password
                ) for txt, clr, data in zip(["Отменить", "Изменить"], [colors.RED, "#16a131"], ["cancel", "change"])),
            actions_alignment=MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def on_focus_textfield(e):
        (user_page_content.tabs[user_page_content.selected_index].content.content.controls[0]
         .controls[0].controls[1].focus())
        (user_page_content.tabs[user_page_content.selected_index].content.content.controls[0]
         .controls[0].controls[1].border_width) = 2
        (user_page_content.tabs[user_page_content.selected_index].content.content.controls[0]
         .controls[0].controls[1].border_color) = (user_page_content.tabs[user_page_content.selected_index]
                                                   .content.content.controls[0].controls[0].controls[0].bgcolor)
        (user_page_content.tabs[user_page_content.selected_index].content.content.controls[0]
         .controls[0].controls[1].update())

    def on_delete_user(e):
        user = data_users[user_page_content.selected_index]
        response = requests.delete(url=server_endpoint + f"/users/{user.id}").json()
        user_page_content.tabs.pop(user_page_content.selected_index)
        page.update()

    def on_add_user(e):
        def on_change_textfield(e):
            # Проверяем, не пустые ли оба поля ввода пароля
            all_fields_filled = all(
                field.value for field in fields if isinstance(field, TextField)
            )

            # Включаем или отключаем кнопку "Задать пароль" в зависимости от заполненности полей
            dlg.actions[1].disabled = not all_fields_filled
            dlg.actions[1].bgcolor = "#16a131" if all_fields_filled is True else "#efefef"
            dlg.actions[1].update()  # Обновляем кнопку для отображения изменений

        def create_user(e):
            if dlg.content.controls[4].controls[1].value == "now":
                if (dlg.content.controls[4].controls[1].content.controls[1].controls[1].controls[1].value
                        == dlg.content.controls[4].controls[1].content.controls[1].controls[2].controls[1].value):
                    new_user = {"fullname": dlg.content.controls[1].controls[1].value,
                                "username": dlg.content.controls[2].controls[1].value,
                                "choosePasswordSetting": dlg.content.controls[4].controls[1].value,
                                "password": (dlg.content.controls[4].controls[1].content.controls[1]
                                             .controls[1].controls[1].value)}
                    # requests.post(server_endpoint + f"/users']}",
                    # headers={'Content-Type': 'application/json'},
                    # data=new_user).json()
                    dlg.open = False
                else:
                    dlg.content.controls[4].controls[1].content.controls[1].controls[2].controls[1].error_text \
                        = "Пароли не совпадают"
                    dlg.content.controls[4].controls[1].content.controls[1].controls[2].controls[1].errol_style \
                        = TextStyle(color=colors.ERROR)
            else:
                new_user = {"fullname": dlg.content.controls[1].controls[1].value,
                            "username": dlg.content.controls[2].controls[1].value,
                            "choosePasswordSetting": dlg.content.controls[4].controls[1].value}
                # requests.post(server_endpoint + f"/users}",
                # headers={'Content-Type': 'application/json'},
                # data=new_user).json()
                dlg.open = False
            page.update()

        def on_cancel(e):
            dlg.open = False
            page.update()

        def on_change_radio(e):
            if e.control.value == "now":
                e.control.content.controls[1].controls[1].controls[1].disabled = False
                e.control.content.controls[1].controls[2].controls[1].disabled = False
                fields.append(e.control.content.controls[1].controls[1].controls[1])
                fields.append(e.control.content.controls[1].controls[2].controls[1])
                e.control.update()
                r = type('e', (object,), {"control": e.control.content.controls[1].controls[1].controls[1]})()
                on_change_textfield(r)
            else:
                (user_page_content.tabs[user_page_content.selected_index].content.content.controls[6]
                 .content.controls[2].trailing.value) = False
                e.control.content.controls[1].controls[1].controls[1].disabled = True
                e.control.content.controls[1].controls[2].controls[1].disabled = True
                fields.remove(e.control.content.controls[1].controls[1].controls[1])
                fields.remove(e.control.content.controls[1].controls[2].controls[1])
                e.control.update()
                r = type('e', (object,), {"control": e.control.content.controls[1].controls[1].controls[1]})()
                on_change_textfield(r)

        dlg = AlertDialog(
            title=Row(controls=[Text(value="Добавить пользователя", size=18)], alignment=MainAxisAlignment.CENTER),
            content_padding=25,
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Text(value="Тип учётной записи"),
                            CupertinoSegmentedButton(
                                selected_index=0,
                                selected_color="#bdbdbd",
                                controls=[
                                    Container(
                                        padding=padding.symmetric(vertical=10, horizontal=30),
                                        content=Text("Обычный", size=16, color=colors.BLACK),
                                    ),
                                    Container(
                                        padding=padding.symmetric(vertical=10, horizontal=30),
                                        content=Text("Администратор", size=16, color=colors.BLACK),
                                    )
                                ],
                                width=580
                            )
                        ],
                        alignment=MainAxisAlignment.END
                    ),
                    Row(
                        controls=[
                            Text(value="Полное имя"),
                            TextField(value=None, data="fullname", on_change=on_change_textfield, width=550),
                        ],
                        alignment=MainAxisAlignment.END
                    ),
                    Row(
                        controls=[
                            Text(value="Имя пользователя"),
                            TextField(value=None, data="username", on_change=on_change_textfield,
                                      helper_text="Используется для именования вашей домашней папки"
                                                  " и не может быть изменено",
                                      width=550),
                        ],
                        alignment=MainAxisAlignment.END
                    ),
                    Row(height=20),
                    Column(
                        controls=[
                            Text(value="Пароль", size=16, weight=FontWeight.BOLD),
                            RadioGroup(
                                value="next_auth",
                                data="chosePasswordSetting",
                                on_change=on_change_radio,
                                content=Column(
                                    controls=[
                                        Radio(value="next_auth",
                                              label="Разрешить пользователю установить"
                                                    " пароль при следующем входе в систему"),
                                        Column(
                                            controls=[
                                                Radio(value="now",
                                                      label="Установить пароль сейчас"),
                                                Row(controls=[
                                                    Text(value="Пароль"),
                                                    TextField(value=None, data="password",
                                                              helper_text="Смешайте заглавные и строчные"
                                                                          " буквы несколько раз",
                                                              on_change=on_change_textfield, width=400, disabled=True,
                                                              password=True, can_reveal_password=True),
                                                ]),
                                                Row(
                                                    controls=[
                                                        Text(value="Подтвердить"),
                                                        TextField(value=None, data="confirm_password", width=400,
                                                                  on_change=on_change_textfield, disabled=True,
                                                                  password=True, can_reveal_password=True),
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ], height=page.window_height * 0.6, width=page.window_width * 0.5,
                horizontal_alignment=CrossAxisAlignment.END
            ),
            actions=list(
                Container(
                    content=Text(value=txt, size=16),
                    bgcolor="#efefef" if data == "add" else clr,
                    border=border.all(width=1, color=colors.BLACK),
                    border_radius=5,
                    padding=padding.symmetric(vertical=10, horizontal=20),
                    margin=margin.only(left=20, right=20),
                    data=data,
                    disabled=True if data == "add" else False,
                    on_hover=on_hover,
                    on_click=on_cancel if data == "cancel" else create_user
                ) for txt, clr, data in zip(["Отменить", "Добавить"], [colors.RED, "#16a131"], ["cancel", "add"])),
            actions_alignment=MainAxisAlignment.END,
        )

        fields = [dlg.content.controls[1].controls[1], dlg.content.controls[2].controls[1]]
        page.dialog = dlg
        dlg.open = True
        page.update()

    user_page_content = Tabs(
        selected_index=0,
        animation_duration=300,
        tab_alignment=TabAlignment.CENTER,
        expand=True,
        tabs=list(
            Tab(
                tab_content=Row(
                    controls=[
                        Container(content=Icon(name=icons.PERSON, color=colors.WHITE),
                                  bgcolor=user_back_colors[i]),
                        Text(value=user.fullName)
                    ]
                ),
                content=Container(
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    Row(controls=[
                                        Container(content=Icon(icons.PERSON, color=colors.WHITE, size=100),
                                                  bgcolor=user_back_colors[i], border_radius=90),
                                        TextField(value=user.fullName, border_radius=4, width=300, data="fullName",
                                                  text_style=TextStyle(size=20, weight=FontWeight.BOLD), border_width=0,
                                                  on_focus=on_focus_textfield, on_submit=on_parameter_change),
                                    ]),
                                    IconButton(icon=icons.EDIT, on_click=on_focus_textfield)
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN
                            ),
                            Row(height=15),
                            Text(value="Параметры аккаунта", size=16, weight=FontWeight.BOLD),
                            Container(
                                content=ListTile(
                                    title=Text(value="Администратор", size=16, weight=FontWeight.BOLD),
                                    subtitle=Text(value="Администраторы могут добавлять и удалять пользователей,"
                                                        " а также изменять настройки всех пользователей."),
                                    trailing=Switch(value=user.role, on_change=on_parameter_change,
                                                    active_color=user_back_colors[i], data="role"),
                                ),
                                border=border.all(width=1),
                                border_radius=8,
                                padding=10
                            ),
                            Row(height=15),
                            Text(value="Аутентификация и вход", size=16, weight=FontWeight.BOLD),
                            Container(
                                content=Column(
                                    controls=[
                                        CupertinoListTile(
                                            title=Text(value="Пароль", size=16, weight=FontWeight.BOLD),
                                            additional_info=Text(value="Установить при следующем входе в систему"
                                            if user.password is None else "•••••",
                                                                 size=14 if user.password is None else 25),
                                            trailing=IconButton(icon=icons.ARROW_FORWARD_IOS,
                                                                on_click=on_change_password)
                                        ),
                                        Divider(),
                                        ListTile(
                                            title=Text(value="Автоматический вход", size=16, weight=FontWeight.BOLD),
                                            trailing=Switch(value=user.autoIn, on_change=on_parameter_change,
                                                            active_color=user_back_colors[i], data="autoIn")
                                        )
                                    ]
                                ),
                                border=border.all(width=1),
                                border_radius=8,
                                padding=10
                            ),
                            Row(height=20),
                            Row(
                                controls=list(
                                    Container(
                                        content=Text(value=txt, color=colors.BLACK, size=15),
                                        alignment=alignment.center,
                                        bgcolor="#efefef" if user.role is False else clr,
                                        border=border.all(width=1, color=colors.BLACK),
                                        border_radius=5,
                                        padding=10,
                                        data=data,
                                        disabled=True if user.role is False else False,
                                        on_hover=on_hover,
                                        on_click=on_delete_user if data == "delete" else on_add_user
                                    ) for txt, clr, data in zip(["Добавить пользователя", "Удалить пользователя"],
                                                                ["#16a131", colors.RED], ["add", "delete"])),
                                alignment=MainAxisAlignment.SPACE_BETWEEN)
                        ],
                        scroll=ScrollMode.AUTO
                    ),
                    alignment=alignment.center,
                    padding=padding.only(left=200, right=200, top=50)
                ),
            ) for i, user in enumerate(data_users)
        ),
    )

    return [user_page_content]
