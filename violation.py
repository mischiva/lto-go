import datetime
import flet as ft
from sidebar import build_sidebar, toggle_sidebar
from styles.fonts import GOOGLE_FONTS


def main(page: ft.Page, sidebar_open=False):
    page.bgcolor = "white"
    page.padding = 0
    page.fonts = GOOGLE_FONTS

    color_primary = "#0038a8"
    color_primary_hover = "#6d8dcc"
    color_border = "#e3e3e3"
    color_field_fill = "#f9f9f9"
    color_text_primary = "#111111"
    color_text_hint = "#5f6368"

    title_style = ft.TextStyle(
        font_family="DM Sans",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=color_primary,
    )
    section_title_style = ft.TextStyle(
        font_family="Roboto",
        size=18,
        weight=ft.FontWeight.W_700,
        color="#111111",
    )
    label_style = ft.TextStyle(
        font_family="Lato",
        size=14,
        weight=ft.FontWeight.W_700,
        color="#222222",
    )
    table_header_style = ft.TextStyle(
        font_family="Lato",
        size=13,
        weight=ft.FontWeight.W_700,
        color="#111111",
    )
    table_data_style = ft.TextStyle(
        font_family="Lato",
        size=13,
        weight=ft.FontWeight.W_500,
        color=color_text_primary,
    )

    blue_button_style = ft.ButtonStyle(
        bgcolor={
            ft.ControlState.DEFAULT: color_primary,
            ft.ControlState.HOVERED: color_primary_hover,
        },
        shape=ft.RoundedRectangleBorder(radius=12),
    )

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
            color=color_text_primary,
            text_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                weight=ft.FontWeight.W_500,
                color=color_text_primary,
            ),
            hint_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                color=color_text_hint,
            ),
            filled=True,
            fill_color=color_field_fill,
            border_color=color_border,
            focused_border_color=color_primary,
            border_radius=12,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=0),
        )

    def dropdown_input(options: list[str]) -> ft.Dropdown:
        return ft.Dropdown(
            options=[ft.DropdownOption(key=opt, text=opt) for opt in options],
            value=options[0] if len(options) > 0 else None,
            color=color_text_primary,
            text_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                weight=ft.FontWeight.W_500,
                color=color_text_primary,
            ),
            filled=True,
            fill_color=color_field_fill,
            border_color=color_border,
            focused_border_color=color_primary,
            border_radius=12,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=8),
            text_size=14,
            menu_height=220,
            dense=True,
        )

    active_date_field = {"target": None}

    def on_date_change(e: ft.Event[ft.DatePicker]):
        target = active_date_field["target"]
        if target and e.control.value:
            target.value = e.control.value.strftime("%m/%d/%Y")
            target.update()

    date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=1900, month=1, day=1),
        last_date=datetime.datetime(year=2100, month=12, day=31),
        on_change=on_date_change,
    )
    page.overlay.append(date_picker)

    def date_input(hint_text: str) -> ft.Row:
        date_field = text_input(hint_text)
        date_field.read_only = True

        def open_picker(e):
            active_date_field["target"] = date_field
            page.show_dialog(date_picker)

        return ft.Row(
            controls=[
                ft.Container(content=date_field, expand=True),
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    icon_color=color_primary,
                    on_click=open_picker,
                    tooltip="Pick date",
                ),
            ],
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def labeled_field(label: str, control: ft.Control, col: int = 6) -> ft.Container:
        return ft.Container(
            col={"xs": 12, "md": col},
            content=ft.Column(
                controls=[
                    ft.Text(label, style=label_style),
                    control,
                ],
                spacing=6,
                tight=True,
            ),
        )

    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Violation", is_open=sidebar_open)

    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e: (toggle_sidebar(sidebar), page.update()),
    )

    form_title = ft.Text("Add violation", style=section_title_style)
    primary_action_label = ft.Text("Save", color="white", weight=ft.FontWeight.W_700)

    def show_add_form(e=None):
        form_title.value = "Add violation"
        form_box.visible = True
        page.update()

    def toggle_add_form(e=None):
        if form_box.visible and form_title.value == "Add violation":
            hide_form()
            return
        show_add_form()

    def show_edit_form(e=None):
        form_title.value = "Edit violation"
        form_box.visible = True
        page.update()

    def hide_form(e=None):
        form_box.visible = False
        page.update()

    filters_row = ft.ResponsiveRow(
        columns=12,
        run_spacing=10,
        controls=[
            ft.Container(
                col={"xs": 12, "md": 4},
                content=ft.TextField(
                    hint_text="Search by driver or plate",
                    prefix_icon=ft.Icons.SEARCH,
                    height=46,
                    color=color_text_primary,
                    text_style=ft.TextStyle(
                        font_family="Lato",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=color_text_primary,
                    ),
                    hint_style=ft.TextStyle(
                        font_family="Lato",
                        size=14,
                        color=color_text_hint,
                    ),
                    filled=True,
                    fill_color=color_field_fill,
                    border_color=color_border,
                    focused_border_color=color_primary,
                    border_radius=12,
                    content_padding=ft.padding.symmetric(horizontal=14, vertical=0),
                ),
            ),
            ft.Container(
                col={"xs": 12, "md": 2},
                content=dropdown_input([
                    "All types",
                    "Overspeeding",
                    "Reckless driving",
                    "No seatbelt",
                ]),
            ),
            ft.Container(
                col={"xs": 12, "md": 2},
                content=dropdown_input([
                    "All statuses",
                    "Unpaid",
                    "Paid",
                    "Contested",
                ]),
            ),
            ft.Container(col={"xs": 0, "md": 2}),
            ft.Container(
                col={"xs": 12, "md": 2},
                content=ft.Button(
                    content=ft.Text(
                        "+ Add violation",
                        style=ft.TextStyle(
                            font_family="Lato",
                            size=14,
                            weight=ft.FontWeight.W_700,
                            color="white",
                        ),
                    ),
                    style=blue_button_style,
                    height=46,
                    width=float("inf"),
                    on_click=toggle_add_form,
                ),
            ),
        ],
    )

    table = ft.DataTable(
        border=ft.border.all(1, color_border),
        border_radius=12,
        horizontal_lines=ft.BorderSide(1, color_border),
        vertical_lines=ft.BorderSide(1, color_border),
        heading_row_height=42,
        data_row_min_height=52,
        data_row_max_height=52,
        heading_row_color="#f4f7fb",
        data_text_style=table_data_style,
        columns=[
            ft.DataColumn(label=ft.Text("Driver", style=table_header_style)),
            ft.DataColumn(label=ft.Text("Plate no.", style=table_header_style)),
            ft.DataColumn(label=ft.Text("Violation type", style=table_header_style)),
            ft.DataColumn(label=ft.Text("Date", style=table_header_style)),
            ft.DataColumn(label=ft.Text("Location", style=table_header_style)),
            ft.DataColumn(label=ft.Text("Fine (PHP)", style=table_header_style)),
            ft.DataColumn(label=ft.Text("Status", style=table_header_style)),
            ft.DataColumn(label=ft.Text("Actions", style=table_header_style)),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Juan Dela Cruz", style=table_data_style)),
                    ft.DataCell(ft.Text("ABC 1234", style=table_data_style)),
                    ft.DataCell(ft.Text("Overspeeding", style=table_data_style)),
                    ft.DataCell(ft.Text("2025-06-10", style=table_data_style)),
                    ft.DataCell(ft.Text("Calamba, Laguna", style=table_data_style)),
                    ft.DataCell(ft.Text("2,000", style=table_data_style)),
                    ft.DataCell(ft.Text("Unpaid", style=table_data_style)),
                    ft.DataCell(
                        ft.Button(
                            content=ft.Text("Edit", color="white", size=12, weight=ft.FontWeight.W_700),
                            on_click=show_edit_form,
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.DEFAULT: color_primary,
                                    ft.ControlState.HOVERED: color_primary_hover,
                                },
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            height=32,
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
                        ft.Text("Violation list", style=section_title_style),
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
        border=ft.border.all(1, color_border),
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
                            on_click=hide_form,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text("Violation details", style=section_title_style),
                ft.ResponsiveRow(
                    columns=12,
                    run_spacing=10,
                    controls=[
                        labeled_field("Driver", text_input(""), col=4),
                        labeled_field("Vehicle (plate no.)", text_input(""), col=4),
                        labeled_field("Violation type", text_input(""), col=4),
                        labeled_field("Date", date_input("mm/dd/yyyy"), col=4),
                        labeled_field("Location", text_input("City / municipality"), col=4),
                        labeled_field("Fine amount (PHP)", text_input("e.g. 2000"), col=4),
                        labeled_field("Apprehending officer", text_input(""), col=4),
                        labeled_field("Status", dropdown_input(["Unpaid", "Paid", "Contested"]), col=4),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Button(
                            content=primary_action_label,
                            style=blue_button_style,
                            on_click=lambda e: None,
                        ),
                        ft.Button(
                            content=ft.Text("Cancel", color="#1f2937", weight=ft.FontWeight.W_700),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.DEFAULT: "#edf2f7"},
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                            on_click=hide_form,
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=12,
        ),
        padding=ft.padding.all(16),
        border=ft.border.all(1, color_border),
        border_radius=14,
        bgcolor="white",
        visible=False,
    )

    main_content = ft.Container(
        content=ft.ListView(
            controls=[
                ft.Row([menu_button], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=6),
                ft.Text("Violation", style=title_style),
                ft.Text(
                    "Record traffic violations committed by drivers.",
                    size=14,
                    color="#4b5563",
                    font_family="Lato",
                ),
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
