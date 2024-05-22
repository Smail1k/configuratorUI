from flet import *

from src.views.base.overall_components import overall
from src.views.base.setting_view import setting
from src.views.base.authentication_view import authorization


def main(page: Page):
    def route_change(route):
        page.window_full_screen = True
        if str(route.route)[1:] in ["authorization", "setting"]:
            appbar.leading = Icon(icons.SETTINGS, color=colors.BLACK)
        else:
            appbar.leading = None

        match page.route:
            case "/authorization":
                page.views.append(
                    View(
                        route="/authorization",
                        appbar=appbar,
                        controls=[authorization(page=page)],
                        vertical_alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    )
                )
            case "/setting":
                page.views.clear()
                page.views.append(
                    View(
                        route="/setting",
                        appbar=appbar,
                        controls=[setting(page=page)]
                    )
                )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.title = "Configuration"

    page.theme_mode = "light"

    icon_darklight, confirm_dialog, appbar = overall(page=page)
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.views.clear()
    page.go("/setting")


app(target=main,
    assets_dir="src/resources", view=AppView.WEB_BROWSER)

#  view=AppView.WEB_BROWSER
