import datetime

import flet as ft

import reports_db
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

    def dropdown_filter_value(value: str | None) -> str:
        value = clean_text(value)
        if value.startswith("All"):
            return ""
        return value

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

    def date_input(hint_text: str):
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
        ), date_field

    def labeled_field(label: str, control: ft.Control, col: int = 6) -> ft.Container:
        return ft.Container(
            col={"xs": 12, "md": col},
            content=ft.Column(
                controls=[
                    ft.Text(label, style=s.LABEL_STYLE),
                    control,
                ],
                spacing=6,
                tight=True,
            ),
        )

    def build_section_header(number: str, title: str) -> ft.Container:
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

    def build_report_table(columns: list[str]) -> ft.DataTable:
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

    def create_pagination_state(table: ft.DataTable):
        items_per_page = ft.Dropdown(
            value="10",
            options=[
                ft.DropdownOption("5"),
                ft.DropdownOption("10"),
                ft.DropdownOption("25"),
                ft.DropdownOption("50"),
            ],
            width=80,
            height=40,
            text_size=12,
            content_padding=ft.Padding.symmetric(horizontal=8, vertical=0),
        )
        prev_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color=s.COLOR_PRIMARY,
            disabled=True,
            tooltip="Previous page",
        )
        next_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            icon_color=s.COLOR_PRIMARY,
            disabled=True,
            tooltip="Next page",
        )
        page_buttons_container = ft.Row(spacing=4, tight=True)
        page_info_text = ft.Text(
            "Page 1 of 1 (0 total items)",
            size=12,
            color=s.COLOR_TEXT_HINT,
            font_family="Lato",
        )
        pagination_controls = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Show:", size=12, color=s.COLOR_TEXT_HINT, font_family="Lato"),
                    items_per_page,
                    ft.Container(width=20),
                    prev_button,
                    page_buttons_container,
                    next_button,
                    ft.Container(width=20),
                    page_info_text,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            border=ft.border.all(1, s.COLOR_BORDER),
            border_radius=8,
            bgcolor="#f8f9fa",
        )
        return {
            "table": table,
            "rows": [],
            "current_page": 1,
            "items_per_page": 10,
            "total_items": 0,
            "items_per_page_dropdown": items_per_page,
            "prev_button": prev_button,
            "next_button": next_button,
            "page_buttons_container": page_buttons_container,
            "page_info_text": page_info_text,
            "pagination_controls": pagination_controls,
        }

    def update_pagination_controls(state):
        total_pages = max(1, (state["total_items"] + state["items_per_page"] - 1) // state["items_per_page"])
        state["page_info_text"].value = f"Page {state['current_page']} of {total_pages} ({state['total_items']} total items)"
        state["page_info_text"].update()

        state["prev_button"].disabled = state["current_page"] <= 1
        state["next_button"].disabled = state["current_page"] >= total_pages
        state["prev_button"].update()
        state["next_button"].update()

        state["page_buttons_container"].controls.clear()
        start_page = max(1, state["current_page"] - 2)
        end_page = min(total_pages, start_page + 4)

        if start_page > 1:
            state["page_buttons_container"].controls.append(
                ft.TextButton("1", on_click=lambda e: go_to_page(state, 1), style=ft.ButtonStyle(color=s.COLOR_PRIMARY))
            )
            if start_page > 2:
                state["page_buttons_container"].controls.append(ft.Text("..."))

        for page_num in range(start_page, end_page + 1):
            is_current = page_num == state["current_page"]
            state["page_buttons_container"].controls.append(
                ft.TextButton(
                    str(page_num),
                    on_click=lambda e, p=page_num: go_to_page(state, p),
                    style=ft.ButtonStyle(
                        bgcolor=s.COLOR_PRIMARY if is_current else ft.Colors.TRANSPARENT,
                    ),
                )
            )

        if end_page < total_pages:
            if end_page < total_pages - 1:
                state["page_buttons_container"].controls.append(ft.Text("..."))
            state["page_buttons_container"].controls.append(
                ft.TextButton(str(total_pages), on_click=lambda e: go_to_page(state, total_pages), style=ft.ButtonStyle(color=s.COLOR_PRIMARY))
            )

        state["page_buttons_container"].update()

    def render_page(state):
        table = state["table"]
        start_idx = (state["current_page"] - 1) * state["items_per_page"]
        end_idx = start_idx + state["items_per_page"]
        page_rows = state["rows"][start_idx:end_idx]

        table.rows.clear()
        for row in page_rows:
            table.rows.append(ft.DataRow(cells=row))
        table.update()
        update_pagination_controls(state)

    def set_rows(state, rows, row_builder):
        state["rows"] = [row_builder(row) for row in rows]
        state["total_items"] = len(state["rows"])
        state["current_page"] = 1
        render_page(state)

    def go_to_page(state, page_num):
        state["current_page"] = page_num
        render_page(state)

    def bind_pagination(state):
        def change_items_per_page(e):
            state["items_per_page"] = int(e.control.value)
            state["current_page"] = 1
            render_page(state)

        def go_previous(e):
            if state["current_page"] > 1:
                go_to_page(state, state["current_page"] - 1)

        def go_next(e):
            total_pages = max(1, (state["total_items"] + state["items_per_page"] - 1) // state["items_per_page"])
            if state["current_page"] < total_pages:
                go_to_page(state, state["current_page"] + 1)

        state["items_per_page_dropdown"].on_select = change_items_per_page
        state["prev_button"].on_click = go_previous
        state["next_button"].on_click = go_next

    def build_report_card(number: str, title: str, description: str, filters: list[ft.Control], state, on_filter) -> ft.Container:
        bind_pagination(state)
        return ft.Container(
            content=ft.Column(
                controls=[
                    build_section_header(number, title),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(description, style=ft.TextStyle(font_family="Lato", size=13, color=s.COLOR_TEXT_HINT)),
                                ft.ResponsiveRow(columns=12, run_spacing=10, controls=filters),
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
                                        on_click=on_filter,
                                    ),
                                    alignment=ft.alignment.Alignment(1, 0),
                                ),
                                ft.Text("Click Filter to load results.", size=12, color=s.COLOR_TEXT_HINT, font_family="Lato"),
                                ft.Container(
                                    content=state["table"],
                                    border=ft.border.all(1, s.COLOR_BORDER),
                                    border_radius=12,
                                    padding=12,
                                    bgcolor="#ffffff",
                                ),
                                state["pagination_controls"],
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

    def clean_text(value: str | None) -> str:
        return value.strip() if value else ""

    def parse_int(value: str | None):
        value = clean_text(value)
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    def parse_date(value: str | None):
        value = clean_text(value)
        if not value:
            return None
        return datetime.datetime.strptime(value, "%m/%d/%Y").date()

    def driver_name(row):
        first = row.get("first_name") or ""
        middle = row.get("middle_name") or ""
        last = row.get("last_name") or ""
        middle_initial = (middle[:1] + ".") if middle else ""
        parts = [last]
        if first:
            parts.append(first)
        if middle_initial:
            parts.append(middle_initial)
        return ", ".join([parts[0], " ".join(parts[1:]).strip()]).strip()

    def vehicle_name(row):
        make = row.get("v_make") or row.get("make") or ""
        model = row.get("v_model") or row.get("model") or ""
        return f"{make} {model}".strip()

    def sex_value(value: str | None) -> str:
        value = clean_text(value)
        if value.startswith("M"):
            return "M"
        if value.startswith("F"):
            return "F"
        return ""

    section_1_search = text_input("Search driver or license no.")
    section_1_license_type = dropdown_input(["All license types", "Non-Professional", "Professional", "Student"])
    section_1_license_status = dropdown_input(["All statuses", "Valid", "Expired", "Suspended", "Revoked"])
    section_1_min_age = text_input("Min age")
    section_1_max_age = text_input("Max age")
    section_1_sex = dropdown_input(["All sex", "M - Male", "F - Female"])
    section_1_table = build_report_table(["License no.", "Driver name", "Age", "Sex", "License type", "Status", "Expiry date"])
    section_1_state = create_pagination_state(section_1_table)

    def load_section_1(e=None):
        rows = reports_db.get_registered_drivers(
            search=clean_text(section_1_search.value),
            license_type=dropdown_filter_value(section_1_license_type.value),
            license_status=dropdown_filter_value(section_1_license_status.value),
            min_age=parse_int(section_1_min_age.value),
            max_age=parse_int(section_1_max_age.value),
            sex=sex_value(dropdown_filter_value(section_1_sex.value)),
        )
        set_rows(
            section_1_state,
            rows,
            lambda row: [
                ft.DataCell(ft.Text(row["license_no"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(driver_name(row), style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(str(row["age"]), style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["sex"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["license_type"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["license_status"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(str(row["license_expire"]), style=s.TABLE_DATA_STYLE)),
            ],
        )

    section_2_search = text_input("Search driver name or license no.")
    section_2_license_no = text_input("Driver license no.")
    section_2_table = build_report_table(["License no.", "Driver name", "Plate no.", "Vehicle type", "Make", "Model", "Color", "Year", "Engine no.", "Chassis no."])
    section_2_state = create_pagination_state(section_2_table)

    def load_section_2(e=None):
        rows = reports_db.get_vehicles_by_driver(
            search=clean_text(section_2_search.value),
            license_no=clean_text(section_2_license_no.value),
        )
        set_rows(
            section_2_state,
            rows,
            lambda row: [
                ft.DataCell(ft.Text(row["license_no"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(driver_name(row), style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["plate_no"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["v_type"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["v_make"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["v_model"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["v_color"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(str(row["v_year"]), style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["engine_no"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["chassis_no"], style=s.TABLE_DATA_STYLE)),
            ],
        )

    section_3_as_of_row, section_3_as_of = date_input("As of date")
    section_3_table = build_report_table(["Plate no.", "Registration no.", "Expiry date", "Vehicle type", "Make/model"])
    section_3_state = create_pagination_state(section_3_table)

    def load_section_3(e=None):
        as_of_date = parse_date(section_3_as_of.value) or datetime.date.today()
        rows = reports_db.get_vehicles_with_expired_registrations(
            as_of_date=as_of_date,
        )
        set_rows(
            section_3_state,
            rows,
            lambda row: [
                ft.DataCell(ft.Text(row["plate_no"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["reg_no"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(str(row["exp_date"]), style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["v_type"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(vehicle_name(row), style=s.TABLE_DATA_STYLE)),
            ],
        )

    section_4_search = text_input("Search driver or license no.")
    section_4_table = build_report_table(["License no.", "Driver name", "Age", "Sex", "License type", "Status", "Expiry date"])
    section_4_state = create_pagination_state(section_4_table)

    def load_section_4(e=None):
        rows = reports_db.get_expired_or_suspended_drivers(
            search=clean_text(section_4_search.value),
        )
        set_rows(
            section_4_state,
            rows,
            lambda row: [
                ft.DataCell(ft.Text(row["license_no"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(driver_name(row), style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(str(row["age"]), style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["sex"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["license_type"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(row["license_status"], style=s.TABLE_DATA_STYLE)),
                ft.DataCell(ft.Text(str(row["license_expire"]), style=s.TABLE_DATA_STYLE)),
            ],
        )

    section_1 = build_report_card(
        "1",
        "View all registered drivers",
        "Filter by license type, license status, age range, and sex.",
        [
            labeled_field("Search", section_1_search, col=4),
            labeled_field("License type", section_1_license_type, col=2),
            labeled_field("License status", section_1_license_status, col=2),
            labeled_field("Min age", section_1_min_age, col=2),
            labeled_field("Max age", section_1_max_age, col=2),
            labeled_field("Sex", section_1_sex, col=2),
        ],
        section_1_state,
        load_section_1,
    )

    section_2 = build_report_card(
        "2",
        "View all vehicles owned by a given driver",
        "Search a driver and list the vehicles they own.",
        [
            labeled_field("Search", section_2_search, col=5),
            labeled_field("Driver license no.", section_2_license_no, col=4),
            ft.Container(col={"xs": 12, "md": 3}),
        ],
        section_2_state,
        load_section_2,
    )

    section_3 = build_report_card(
        "3",
        "View all vehicles with expired registrations",
        "Pick a date and list vehicles whose registration expired before that date.",
        [
            labeled_field("As of date", section_3_as_of_row, col=4),
            ft.Container(col={"xs": 12, "md": 8}),
        ],
        section_3_state,
        load_section_3,
    )

    section_4 = build_report_card(
        "4",
        "View all drivers with expired or suspended licenses",
        "List drivers whose license status is expired or suspended.",
        [
            labeled_field("Search", section_4_search, col=4),
            ft.Container(col={"xs": 12, "md": 8}),
        ],
        section_4_state,
        load_section_4,
    )

    def build_placeholder_report_card(number: str, title: str, description: str, message: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    build_section_header(number, title),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(description, style=ft.TextStyle(font_family="Lato", size=13, color=s.COLOR_TEXT_HINT)),
                                ft.Container(
                                    content=ft.Text(
                                        message,
                                        style=ft.TextStyle(
                                            font_family="Lato",
                                            size=13,
                                            color=s.COLOR_TEXT_PRIMARY,
                                            weight=ft.FontWeight.W_600,
                                        ),
                                    ),
                                    padding=16,
                                    bgcolor="#f8f9fa",
                                    border_radius=12,
                                    border=ft.border.all(1, s.COLOR_BORDER),
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

    section_5 = build_placeholder_report_card(
        "5",
        "View all traffic violations committed by a given driver",
        "",
        "Gabe can u do this after u finish violations (di ko magawa since violations need nito)",
    )

    section_6 = build_placeholder_report_card(
        "6",
        "View the total number of violations per violation type",
        "",
        "Gabe can u do this after u finish violations (di ko magawa since violations need nito)",
    )

    section_7 = build_placeholder_report_card(
        "7",
        "View all vehicles involved in violations",
        "",
        "Gabe can u do this after u finish violations (di ko magawa since violations need nito)",
    )

    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([menu_button], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=12),
                ft.Text("Generate reports", style=s.TITLE_STYLE),
                ft.Container(height=12),
                ft.Column(controls=[section_1, section_2, section_3, section_4, section_5, section_6, section_7], spacing=18),
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
