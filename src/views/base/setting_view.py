import importlib.util
from flet import *

from src.resources.static_data import components_sidebar


def setting(page: Page):
    selected_sidebar_item = None

    def on_hover(e):
        if page.theme_mode == "light":
            e.control.bgcolor = "#dcdcdc" if e.data == "true" else page.bgcolor
        else:
            e.control.bgcolor = "#636363" if e.data == "true" else page.bgcolor

        e.control.update()

    # def on_hover_save(e):
    #     e.control.bgcolor = colors.GREY_400 if e.data == "true" else "#efefef"
    #     e.control.update()

    def on_click(e: ContainerTapEvent):
        nonlocal selected_sidebar_item

        if selected_sidebar_item is not None:
            for item in sidebar.content.controls:
                if item.data == selected_sidebar_item:
                    item.bgcolor = None
                    item.on_hover = on_hover

        selected_sidebar_item = e.control.data
        e.control.bgcolor = colors.GREY_400
        e.control.on_hover = None

        title_row.controls[0].value = e.control.content.controls[1].value

        # Загрузка модуля
        spec = importlib.util.spec_from_file_location(name=e.control.data + '_page',
                                                      location=f"src/views/pages/{e.control.data}_page.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Получение атрибута из модуля
        function = getattr(module, e.control.data)

        content_column.controls = [Container(content=ProgressRing(),
                                             alignment=alignment.center,
                                             expand=True
                                             )]
        page.update()

        content_column.controls = function(page)
        page.update()

    sidebar = Container(
        content=Column(
            controls=list(
                Container(
                    content=Row(
                        controls=[Icon(name=component[2], color=colors.BLACK)
                                  if "png" not in component[2] else Image(src=component[2], color=colors.BLACK),
                                  Text(value=component[0], size=17)],
                        expand_loose=True
                    ),
                    data=component[1],
                    padding=padding.only(left=5),
                    border_radius=5,
                    on_click=on_click,
                    on_hover=on_hover,
                    height=100
                ) for component in components_sidebar),
        ),
        padding=padding.only(right=10),
        border=Border(right=BorderSide(width=1, color="#c9c9c9")),
        expand=True
    )

    title_row = Row(
        controls=[
            Text(value="Выберите пункт", size=25, text_align=alignment.center),
        ],
        alignment=MainAxisAlignment.CENTER
    )

    # save_button = get_save_button()
    # save_button.controls[0].on_hover = on_hover_save

    content_column = Column(spacing=15, expand=True)

    body_column = Column(controls=[title_row, Divider(thickness=1, height=15), content_column], expand=3)

    setting_row = Row(controls=[sidebar, body_column], spacing=0, expand=True)

    return setting_row
