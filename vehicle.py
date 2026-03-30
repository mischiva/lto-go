import flet as ft
from sidebar import build_sidebar, toggle_sidebar
from styles.fonts import GOOGLE_FONTS
from styles.vehicle_styles import (
    COLOR_PRIMARY,
    COLOR_BORDER,
    COLOR_FIELD_FILL,
    COLOR_DANGER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_HINT,
    TITLE_STYLE,
    SECTION_TITLE_STYLE,
    LABEL_STYLE,
    TABLE_HEADER_STYLE,
    TABLE_DATA_STYLE,
    BLUE_BUTTON_STYLE,
    DANGER_BUTTON_STYLE,
)


def main(page: ft.Page, sidebar_open=False):
    page.bgcolor = "white"
    page.padding = 0
    page.fonts = GOOGLE_FONTS


    def go_to(screen_main, keep_sidebar_open=False):
        page.controls.clear()
        screen_main(page, sidebar_open=keep_sidebar_open)
        page.update()

    def go_to_sign_in():
        from sign_in import main as sign_in_main
        page.controls.clear()
        sign_in_main(page)
        page.update()

    def on_menu_item_click(item_name):
        if item_name == "__close__":
            toggle_sidebar(sidebar)
            return
        if item_name == "Sign out":
            go_to_sign_in()
            return

        if item_name == "Home":
            from home import main as home_main
            go_to(home_main, keep_sidebar_open=True)
        elif item_name == "Driver":
            from driver import main as driver_main
            go_to(driver_main, keep_sidebar_open=True)
        elif item_name == "Vehicle":
            from vehicle import main as vehicle_main
            go_to(vehicle_main, keep_sidebar_open=True)
        elif item_name == "Registration":
            from registration import main as registration_main
            go_to(registration_main, keep_sidebar_open=True)
        elif item_name == "Violation":
            from violation import main as violation_main
            go_to(violation_main, keep_sidebar_open=True)
        elif item_name == "Generate reports":
            from reports import main as reports_main
            go_to(reports_main, keep_sidebar_open=True)

    def text_input(hint_text: str) -> ft.TextField:
        return ft.TextField(
            hint_text=hint_text,
            height=46,
            color=COLOR_TEXT_PRIMARY,
            text_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                weight=ft.FontWeight.W_500,
                color=COLOR_TEXT_PRIMARY,
            ),
            hint_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                color=COLOR_TEXT_HINT,
            ),
            filled=True,
            fill_color=COLOR_FIELD_FILL,
            border_color=COLOR_BORDER,
            focused_border_color=COLOR_PRIMARY,
            border_radius=12,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=0),
        )

    def dropdown_input(options: list[str]) -> ft.Dropdown:
        return ft.Dropdown(
            options=[ft.DropdownOption(key=opt, text=opt) for opt in options],
            value=options[0] if len(options) > 0 else None,
            color=COLOR_TEXT_PRIMARY,
            text_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                weight=ft.FontWeight.W_500,
                color=COLOR_TEXT_PRIMARY,
            ),
            filled=True,
            fill_color=COLOR_FIELD_FILL,
            border_color=COLOR_BORDER,
            focused_border_color=COLOR_PRIMARY,
            border_radius=12,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=8),
            text_size=14,
            menu_height=220,
            dense=True,
        )

    def labeled_field(label: str, control: ft.Control, col: int = 6) -> ft.Container:
        return ft.Container(
            col={"xs": 12, "md": col},
            content=ft.Column(
                controls=[
                    ft.Text(label, style=LABEL_STYLE),
                    control,
                ],
                spacing=6,
                tight=True,
            ),
        )

    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Vehicle", is_open=sidebar_open)

    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e: (toggle_sidebar(sidebar), page.update()),
    )

    form_title = ft.Text("Add vehicle", style=SECTION_TITLE_STYLE)
    primary_action_label = ft.Text("Add", color="white", weight=ft.FontWeight.W_700)

    def show_add_form(e=None):
        form_title.value = "Add vehicle"
        primary_action_label.value = "Add"
        form_box.visible = True
        page.update()

    def toggle_add_form(e=None):
        if form_box.visible and form_title.value == "Add vehicle":
            hide_edit_form()
            return
        show_add_form()

    def show_edit_form(e=None):
        form_title.value = "Add vehicle"
        primary_action_label.value = "Add"
        form_box.visible = True
        page.update()

    def hide_edit_form(e=None):
        form_box.visible = False
        page.update()

    filters_row = ft.ResponsiveRow(
        columns=12,
        run_spacing=10,
        controls=[
            ft.Container(
                col={"xs": 12, "md": 4},
                content=ft.TextField(
                    hint_text="Search by plate or engine no.",
                    prefix_icon=ft.Icons.SEARCH,
                    height=46,
                    color=COLOR_TEXT_PRIMARY,
                    text_style=ft.TextStyle(
                        font_family="Lato",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    hint_style=ft.TextStyle(
                        font_family="Lato",
                        size=14,
                        color=COLOR_TEXT_HINT,
                    ),
                    filled=True,
                    fill_color=COLOR_FIELD_FILL,
                    border_color=COLOR_BORDER,
                    focused_border_color=COLOR_PRIMARY,
                    border_radius=12,
                    content_padding=ft.padding.symmetric(horizontal=14, vertical=0),
                ),
            ),
            ft.Container(
                col={"xs": 12, "md": 2},
                content=dropdown_input([
                    "All types",
                    "Private car",
                    "Motorcycle",
                    "PUV",
                ]),
            ),
            ft.Container(col={"xs": 0, "md": 3}),
            ft.Container(
                col={"xs": 6, "md": 1},
                content=ft.Button(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.FILTER_ALT, color="white", size=16),
                            ft.Text(
                                "Filter",
                                style=ft.TextStyle(
                                    font_family="Lato",
                                    size=13,
                                    weight=ft.FontWeight.W_700,
                                    color="white",
                                ),
                            ),
                        ],
                        spacing=6,
                        tight=True,
                    ),
                    style=BLUE_BUTTON_STYLE,
                    height=46,
                    width=float("inf"),
                    on_click=lambda e: None,
                ),
            ),
            ft.Container(
                col={"xs": 6, "md": 2},
                content=ft.Button(
                    content=ft.Text(
                        "+ Add vehicle",
                        style=ft.TextStyle(
                            font_family="Lato",
                            size=14,
                            weight=ft.FontWeight.W_700,
                            color="white",
                        ),
                    ),
                    style=BLUE_BUTTON_STYLE,
                    height=46,
                    width=float("inf"),
                    on_click=toggle_add_form,
                ),
            ),
        ],
    )

    table = ft.DataTable(
        border=ft.border.all(1, COLOR_BORDER),
        border_radius=12,
        horizontal_lines=ft.BorderSide(1, COLOR_BORDER),
        vertical_lines=ft.BorderSide(1, COLOR_BORDER),
        heading_row_height=42,
        data_row_min_height=52,
        data_row_max_height=52,
        heading_row_color="#f4f7fb",
        data_text_style=TABLE_DATA_STYLE,
        columns=[
            ft.DataColumn(label=ft.Text("Plate no.", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Make / model", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Year", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Type", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Owner", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Actions", style=TABLE_HEADER_STYLE)),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("ABC 1234", style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text("Toyota Vios", style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text("2020", style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text("Private car", style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text("Juan Dela Cruz", style=TABLE_DATA_STYLE)),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.Button(
                                    content=ft.Text("Edit", color="white", size=12, weight=ft.FontWeight.W_700),
                                    on_click=show_edit_form,
                                    style=BLUE_BUTTON_STYLE,
                                    height=32,
                                ),
                                ft.Button(
                                    content=ft.Text("Delete", color="white", size=12, weight=ft.FontWeight.W_700),
                                    on_click=lambda e: None,
                                    style=DANGER_BUTTON_STYLE,
                                    height=32,
                                ),
                            ],
                            spacing=6,
                            tight=True,
                        )
                    ),
                ]
            ),
        ],
    )

    table_block = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Vehicle list", style=SECTION_TITLE_STYLE),
                        ft.Text(
                            "Manage records from this screen",
                            size=12,
                            color="#6b7280",
                            font_family="Lato",
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            table,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    border_radius=12,
                ),
            ],
            spacing=10,
        ),
        padding=ft.padding.all(16),
        border=ft.border.all(1, COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
    )

    form_box = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        form_title,
                        ft.Button(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.CLOSE, color="#1f2937", size=16),
                                    ft.Text("Close", color="#1f2937", size=12, weight=ft.FontWeight.W_700),
                                ],
                                spacing=4,
                                tight=True,
                            ),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.DEFAULT: "#edf2f7"},
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            height=34,
                            on_click=hide_edit_form,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text("Vehicle details", style=SECTION_TITLE_STYLE),
                ft.ResponsiveRow(
                    columns=12,
                    run_spacing=10,
                    controls=[
                        labeled_field("Plate number", text_input("e.g. ABC 1234"), col=4),
                        labeled_field("Engine number", text_input(""), col=4),
                        labeled_field("Chassis number", text_input(""), col=4),
                        labeled_field("Vehicle type", dropdown_input(["Motorcycle", "Private car", "PUV"]), col=4),
                        labeled_field("Make", text_input("e.g. Toyota"), col=4),
                        labeled_field("Model", text_input("e.g. Vios"), col=4),
                        labeled_field("Year", text_input("e.g. 2020"), col=4),
                        labeled_field("Color", text_input("e.g. White"), col=4),
                        labeled_field("Registered owner", dropdown_input(["Juan Dela Cruz", "Ana Lim", "Pedro Reyes"]), col=4),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Button(
                            content=primary_action_label,
                            style=BLUE_BUTTON_STYLE,
                            on_click=lambda e: None,
                        ),
                        ft.Button(
                            content=ft.Text("Delete", color="white", weight=ft.FontWeight.W_700),
                            style=DANGER_BUTTON_STYLE,
                            on_click=lambda e: None,
                        ),
                        ft.Button(
                            content=ft.Text("Cancel", color="#1f2937", weight=ft.FontWeight.W_700),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.DEFAULT: "#edf2f7"},
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                            on_click=hide_edit_form,
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=12,
        ),
        padding=ft.padding.all(16),
        border=ft.border.all(1, COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
        visible=False,
    )

    main_content = ft.Container(
        content=ft.ListView(
            controls=[
                ft.Row([menu_button], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=6),
                ft.Text("Vehicle", style=TITLE_STYLE),
                filters_row,
                table_block,
                form_box,
            ],
            spacing=16,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=30),
        expand=True,
    )

    page.add(
        ft.Stack(
            controls=[
                main_content,
                sidebar,
            ],
            expand=True,
        )
    )
