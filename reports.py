import datetime

import flet as ft

from sidebar import build_sidebar, toggle_sidebar
from styles.fonts import GOOGLE_FONTS
from styles import registration_styles as s


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
            page.update()

    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Generate reports", is_open=sidebar_open)

    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e: (toggle_sidebar(sidebar), page.update()),
    )

    def text_input(hint_text: str) -> ft.TextField:
        # text field styling so every report input looks the same
        return ft.TextField(
            hint_text=hint_text,
            height=46,
            color=s.COLOR_TEXT_PRIMARY,
            text_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                weight=ft.FontWeight.W_500,
                color=s.COLOR_TEXT_PRIMARY,
            ),
            hint_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                color=s.COLOR_TEXT_HINT,
            ),
            filled=True,
            fill_color=s.COLOR_FIELD_FILL,
            border_color=s.COLOR_BORDER,
            focused_border_color=s.COLOR_PRIMARY,
            border_radius=12,
            content_padding=ft.Padding.symmetric(horizontal=14, vertical=0),
        )

    def dropdown_input(options: list[str], value: str | None = None) -> ft.Dropdown:
        # dropdown styling for filter controls
        return ft.Dropdown(
            options=[ft.DropdownOption(key=opt, text=opt) for opt in options],
            value=value if value is not None else (options[0] if options else None),
            color=s.COLOR_TEXT_PRIMARY,
            text_style=ft.TextStyle(
                font_family="Lato",
                size=14,
                weight=ft.FontWeight.W_500,
                color=s.COLOR_TEXT_PRIMARY,
            ),
            filled=True,
            fill_color=s.COLOR_FIELD_FILL,
            border_color=s.COLOR_BORDER,
            focused_border_color=s.COLOR_PRIMARY,
            border_radius=12,
            content_padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            text_size=14,
            menu_height=220,
            dense=True,
        )

    active_date_field = {"target": None}

    def on_date_change(e: ft.Event[ft.DatePicker]):
        # write the picked date back into whateverr field opened the calendar
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
        # date input with a calendar
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
                    icon_color=s.COLOR_PRIMARY,
                    on_click=open_picker,
                    tooltip="Pick date",
                ),
            ],
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # PLACEHOLDER PLACEHOLDER PLACEHOLDER WALA PANG SQL CODE EMPTY TABLE ONLYYYYYYYY
    # PLACEHOLDER PLACEHOLDER PLACEHOLDER WALA PANG SQL CODE EMPTY TABLE ONLYYYYYYYY
    # PLACEHOLDER PLACEHOLDER PLACEHOLDER WALA PANG SQL CODE EMPTY TABLE ONLYYYYYYYY
    # PLACEHOLDER PLACEHOLDER PLACEHOLDER WALA PANG SQL CODE EMPTY TABLE ONLYYYYYYYY
    # PLACEHOLDER PLACEHOLDER PLACEHOLDER WALA PANG SQL CODE EMPTY TABLE ONLYYYYYYYY
    # PLACEHOLDER PLACEHOLDER PLACEHOLDER WALA PANG SQL CODE EMPTY TABLE ONLYYYYYYYY
    # PLACEHOLDER PLACEHOLDER PLACEHOLDER WALA PANG SQL CODE EMPTY TABLE ONLYYYYYYYY

    def build_empty_report_table(columns: list[str]) -> ft.DataTable:
        return ft.DataTable(
            border=ft.border.all(1, s.COLOR_BORDER),
            border_radius=12,
            horizontal_lines=ft.BorderSide(1, s.COLOR_BORDER),
            vertical_lines=ft.BorderSide(1, s.COLOR_BORDER),
            heading_row_height=42,
            data_row_min_height=52,
            data_row_max_height=52,
            heading_row_color="#f4f7fb",
            data_text_style=s.TABLE_DATA_STYLE,
            columns=[ft.DataColumn(label=ft.Text(column, style=s.TABLE_HEADER_STYLE)) for column in columns],
            rows=[],
        )

    def build_section_header(number: str, title: str) -> ft.Container:
        # header bar for each report section 
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(number, color="white", weight=ft.FontWeight.W_700),
                        width=34,
                        height=34,
                        alignment=ft.alignment.Alignment(0, 0),
                        bgcolor=s.COLOR_PRIMARY,
                        border_radius=999,
                    ),
                    ft.Text(
                        title,
                        style=ft.TextStyle(
                            font_family="Roboto",
                            size=18,
                            weight=ft.FontWeight.W_700,
                            color="#111111",
                        ),
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
            bgcolor="#f8faff",
            border=ft.border.only(bottom=ft.BorderSide(1, s.COLOR_BORDER)),
        )

    def build_report_section(number: str, title: str, description: str, filters: list[ft.Control], columns: list[str]) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    build_section_header(number, title),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    description,
                                    style=ft.TextStyle(font_family="Lato", size=13, color=s.COLOR_TEXT_HINT),
                                ),
                                ft.ResponsiveRow(
                                    columns=12,
                                    run_spacing=10,
                                    controls=filters,
                                ),
                                ft.Container(
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
                                        style=ft.ButtonStyle(
                                            bgcolor={
                                                ft.ControlState.DEFAULT: s.COLOR_PRIMARY,
                                                ft.ControlState.HOVERED: s.COLOR_PRIMARY_HOVER,
                                            },
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                        ),
                                        height=42,
                                        width=140,
                                        on_click=lambda e: None,
                                    ),
                                    alignment=ft.alignment.Alignment(1, 0),
                                ),
                                ft.Container(height=4),
                                ft.Container(
                                    content=build_empty_report_table(columns),
                                    border=ft.border.all(1, s.COLOR_BORDER),
                                    border_radius=12,
                                    padding=12,
                                    bgcolor="#ffffff",
                                ),
                            ],
                            spacing=12,
                        ),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=16),
                    ),
                ],
                spacing=0,
            ),
            border=ft.border.all(1, s.COLOR_BORDER),
            border_radius=14,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor="#ffffff",
        )

    report_sections = [
        build_report_section(
            "1",
            "View all registered drivers",
            "Filter by license type, license status, age range, and sex.",
            [
                ft.Container(col={"xs": 12, "md": 4}, content=text_input("Search driver or license no.")),
                ft.Container(col={"xs": 12, "md": 2}, content=dropdown_input(["All license types", "Non-Professional", "Professional", "Student"])),
                ft.Container(col={"xs": 12, "md": 2}, content=dropdown_input(["All statuses", "Valid", "Expired", "Suspended"])),
                ft.Container(col={"xs": 6, "md": 2}, content=text_input("Min age")),
                ft.Container(col={"xs": 6, "md": 2}, content=text_input("Max age")),
                ft.Container(col={"xs": 12, "md": 2}, content=dropdown_input(["All sex", "M - Male", "F - Female"])),
            ],
            ["License no.", "Driver name", "Age", "Sex", "License type", "Status"],
        ),
        build_report_section(
            "2",
            "View all vehicles owned by a given driver",
            "Choose the driver and inspect the vehicles they own.",
            [
                ft.Container(col={"xs": 12, "md": 6}, content=text_input("Search driver name or license no.")),
                ft.Container(col={"xs": 12, "md": 3}, content=text_input("Driver ID / license no.")),
                ft.Container(col={"xs": 12, "md": 3}, content=dropdown_input(["All vehicle types", "Private car", "Motorcycle", "PUV"])),
            ],
            ["Plate no.", "Vehicle type", "Make / model", "Year", "Owner"],
        ),
        build_report_section(
            "3",
            "View all vehicles with expired registrations",
            "Check all vehicles whose registration is expired as of the selected date.",
            [
                ft.Container(col={"xs": 12, "md": 4}, content=text_input("Search plate or registration no.")),
                ft.Container(col={"xs": 12, "md": 4}, content=date_input("As of date")),
                ft.Container(col={"xs": 12, "md": 4}, content=dropdown_input(["All statuses", "Active", "Expired", "Suspended"])),
            ],
            ["Plate no.", "Owner", "Registration no.", "Expiry date", "Status"],
        ),
        build_report_section(
            "4",
            "View all drivers with expired or suspended licenses",
            "List drivers whose license is either expired or suspended.",
            [
                ft.Container(col={"xs": 12, "md": 5}, content=text_input("Search driver or license no.")),
                ft.Container(col={"xs": 12, "md": 3}, content=dropdown_input(["Expired", "Suspended", "Expired or Suspended"], value="Expired or Suspended")),
                ft.Container(col={"xs": 12, "md": 2}, content=dropdown_input(["All sex", "M - Male", "F - Female"])),
                ft.Container(col={"xs": 12, "md": 2}, content=text_input("Age range")),
            ],
            ["License no.", "Driver name", "License type", "Status", "Expiry date"],
        ),
        build_report_section(
            "5",
            "View all traffic violations committed by a given driver",
            "Use the date range to narrow violations for a specific driver.",
            [
                ft.Container(col={"xs": 12, "md": 4}, content=text_input("Search driver name or license no.")),
                ft.Container(col={"xs": 12, "md": 3}, content=date_input("From date")),
                ft.Container(col={"xs": 12, "md": 3}, content=date_input("To date")),
                ft.Container(col={"xs": 12, "md": 2}, content=dropdown_input(["All types", "Overspeeding", "Reckless driving", "No seatbelt"])),
            ],
            ["Driver", "Violation type", "Date", "Plate no.", "Location"],
        ),
        build_report_section(
            "6",
            "View the total number of violations per violation type",
            "Pick a year and show how many violations each type has.",
            [
                ft.Container(col={"xs": 12, "md": 4}, content=text_input("Year")),
                ft.Container(col={"xs": 12, "md": 4}, content=dropdown_input(["All types", "Overspeeding", "Reckless driving", "No seatbelt"])),
                ft.Container(col={"xs": 12, "md": 4}, content=text_input("Search type or keyword")),
            ],
            ["Violation type", "Total count"],
        ),
        build_report_section(
            "7",
            "View all vehicles involved in violations",
            "Filter the result by city or region.",
            [
                ft.Container(col={"xs": 12, "md": 5}, content=text_input("City or region")),
                ft.Container(col={"xs": 12, "md": 4}, content=text_input("Search plate or driver")),
                ft.Container(col={"xs": 12, "md": 3}, content=dropdown_input(["All types", "Overspeeding", "Reckless driving", "No seatbelt"])),
            ],
            ["Plate no.", "Driver", "Violation type", "Date", "City / region"],
        ),
    ]

    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([menu_button], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=12),
                ft.Text("Generate reports", style=s.TITLE_STYLE),
                ft.Container(height=12),
                ft.Column(controls=report_sections, spacing=18),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.Padding.symmetric(horizontal=40, vertical=30),
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
