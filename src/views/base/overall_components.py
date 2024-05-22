import requests
from flet import *

from config import server_endpoint


def overall(page: Page):
    def change_theme(e):
        page.splash.visible = True
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.views[-1].appbar.bgcolor = "#9e9e9e" if page.theme_mode == "dark" else "#ebebeb"
        icon_darklight.selected = not icon_darklight.selected
        for item in page.views[-1].controls[0].controls[0].content.controls:
            item.content.controls[0].color = colors.WHITE if page.theme_mode == "dark" else colors.BLACK
        page.splash.visible = False
        page.update()

    def change_clicker(e):
        def enter(e: ContainerTapEvent):
            if not dlg.content.controls[0].value:
                dlg.content.controls[0].error_text = "Пожалуйста, введите свой логин"
                page.update()
                return
            else:
                dlg.content.controls[0].error_text = None
                page.update()

            if not dlg.content.controls[1].value:
                dlg.content.controls[1].error_text = "Пожалуйста, введите свой пароль"
                page.update()
                return
            else:
                dlg.error_text = None
                page.update()

            page.go("/setting")
            # response = requests.post(url=server_endpoint + "/authorization",
            #                                                    data={'username': login_auth.value,
            #                                                          'password': password_auth.value})

        dlg = AlertDialog(
            title=Text(value="Сменить пользователя", size=18),
            content=Column(
                controls=[
                    TextField(value=None, hint_text="Логин", data="login"),
                    TextField(value=None, hint_text="Пароль", data="password",
                              password=True, can_reveal_password=True),
                ],
                height=130, width=330),
            actions=[
                TextButton(content=Text(value="Войти", size=20, text_align=TextAlign.CENTER), on_click=enter)
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def check_exit_clicked(e):
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    def yes_click_confirm(e):
        page.views.clear()
        page.go("/authorization")

    def no_click_confirm(e):
        confirm_dialog.open = False
        page.update()

    icon_darklight = IconButton(
        on_click=change_theme,
        icon="dark_mode",
        selected_icon="light_mode",
        style=ButtonStyle(color=colors.BLACK)
    )

    appbar = AppBar(
        center_title=False,
        title=Text("Настройки", color=colors.BLACK),
        bgcolor="#ebebeb",
        actions=[
            icon_darklight,
            IconButton(icon=icons.CHANGE_CIRCLE, on_click=change_clicker, style=ButtonStyle(color=colors.BLACK)),
            IconButton(icon=icons.EXIT_TO_APP, on_click=check_exit_clicked, style=ButtonStyle(color=colors.BLACK))
        ],

    )

    confirm_dialog = AlertDialog(
        modal=True,
        title=Text("Пожалуйста, подтвердите"),
        content=Text("Вы действительно хотите выйти?"),
        actions=[
            ElevatedButton("Да", on_click=yes_click_confirm),
            OutlinedButton("Нет", on_click=no_click_confirm),
        ],
        actions_alignment=MainAxisAlignment.END,
    )

    return icon_darklight, confirm_dialog, appbar


# def get_save_button():
#
#     save_button = Row(
#         controls=[
#             Container(
#                 content=Text(value="Сохранить", color=colors.BLACK, size=15),
#                 alignment=alignment.center,
#                 width=130, height=35,
#                 bgcolor="#efefef",
#                 border=border.all(width=1, color=colors.BLACK),
#                 border_radius=border_radius.all(5),
#                 margin=margin.only(0, 0, 30, 20)
#             )],
#         alignment=MainAxisAlignment.END,
#         vertical_alignment=CrossAxisAlignment.END,
#     )
#
#     return save_button
