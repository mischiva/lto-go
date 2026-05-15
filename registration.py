import datetime

import flet as ft

import registration_db
import vehicle_db
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
            from reports import main as reports_main

            go_to(reports_main, keep_sidebar_open=True)

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

    def dropdown_input(options: list[str]) -> ft.Dropdown:
        return ft.Dropdown(
            options=[ft.DropdownOption(key=opt, text=opt) for opt in options],
            value=options[0] if options else None,
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
        error_text = ft.Text("", size=11, color="#B42318")

        def open_picker(e):
            active_date_field["target"] = date_field
            page.show_dialog(date_picker)

        row = ft.Row(
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
        row.error = error_text
        row.date_field = date_field
        return row

    def labeled_field(label: str, control: ft.Control, col: int = 6) -> ft.Container:
        controls = [ft.Text(label, style=s.LABEL_STYLE), control]
        err = getattr(control, "error", None)
        if err is not None:
            controls.append(err)

        return ft.Container(
            col={"xs": 12, "md": col},
            content=ft.Column(
                controls=controls,
                spacing=6,
                tight=True,
            ),
        )

    def format_date_value(value):
        if not value:
            return ""
        if isinstance(value, str):
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
            except Exception:
                return value
        return value.strftime("%m/%d/%Y")

    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Registration", is_open=sidebar_open)

    menu_button = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e: (toggle_sidebar(sidebar), page.update()),
    )

    form_title = ft.Text("Add registration", style=s.SECTION_TITLE_STYLE)
    primary_action_label = ft.Text("Save", color="white", weight=ft.FontWeight.W_700)

    current_page = {"value": 1}
    items_per_page = {"value": 10}
    total_items = {"value": 0}
    all_rows_data = []
    editingRegNo = {"value": None}

    def error_text():
        return ft.Text("", size=11, color="#B42318")

    fRegNo = text_input("e.g. 48290173")
    fRegNo.error = error_text()
    fPlateNo = text_input("e.g. ABC 1234")
    fPlateNo.error = error_text()
    fRegDate = date_input("mm/dd/yyyy")
    fExpiryDate = date_input("mm/dd/yyyy")
    fStatus = dropdown_input(["Active", "Expired", "Suspended"])
    fStatus.error = error_text()

    searchInput = text_input("Search by reg no., plate, vehicle, or owner")
    searchInput.prefix_icon = ft.Icons.SEARCH
    statusInput = dropdown_input(["All statuses", "Active", "Expired", "Suspended"])

    def clear_errors():
        for control in (fRegNo, fPlateNo, fRegDate, fExpiryDate, fStatus):
            if getattr(control, "error", None) is not None:
                control.error.value = ""

    def reset_form_values():
        editingRegNo["value"] = None
        fRegNo.value = ""
        fPlateNo.value = ""
        fRegDate.date_field.value = ""
        fExpiryDate.date_field.value = ""
        fStatus.value = "Active"
        clear_errors()

    def show_add_form(e=None):
        reset_form_values()
        form_title.value = "Add registration"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def show_edit_form(reg_no):
        row = registration_db.getRegistration(reg_no)
        if not row:
            page.snack_bar = ft.SnackBar(ft.Text("Registration not found."))
            page.snack_bar.open = True
            page.update()
            return

        editingRegNo["value"] = reg_no
        clear_errors()
        fRegNo.value = row["reg_no"]
        fPlateNo.value = row["plate_no"]
        fRegDate.date_field.value = format_date_value(row["reg_date"])
        fExpiryDate.date_field.value = format_date_value(row["expiry_date"])
        fStatus.value = row["status"]
        form_title.value = "Edit registration"
        primary_action_label.value = "Update"
        form_box.visible = True
        page.update()

    def toggle_add_form(e=None):
        if form_box.visible and form_title.value == "Add registration":
            hide_form()
            return
        show_add_form()

    def hide_form(e=None):
        form_box.visible = False
        page.update()

    def filter_registrations(e=None):
        current_page["value"] = 1
        loadTable(searchInput.value or "", statusInput.value or "", 1, items_per_page["value"])

    filters_row = ft.ResponsiveRow(
        columns=12,
        run_spacing=10,
        controls=[
            ft.Container(col={"xs": 12, "md": 4}, content=searchInput),
            ft.Container(col={"xs": 12, "md": 2}, content=statusInput),
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
                    width=float("inf"),
                    on_click=filter_registrations,
                    style=ft.ButtonStyle(
                        bgcolor={
                            ft.ControlState.DEFAULT: s.COLOR_PRIMARY,
                            ft.ControlState.HOVERED: s.COLOR_PRIMARY_HOVER,
                        },
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                    height=42,
                ),
            ),
            ft.Container(
                col={"xs": 6, "md": 2},
                content=ft.Button(
                    content=ft.Text(
                        "+ New registration",
                        style=ft.TextStyle(
                            font_family="Lato",
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color="white",
                        ),
                    ),
                    width=float("inf"),
                    on_click=toggle_add_form,
                    style=ft.ButtonStyle(
                        bgcolor={
                            ft.ControlState.DEFAULT: s.COLOR_PRIMARY,
                            ft.ControlState.HOVERED: s.COLOR_PRIMARY_HOVER,
                        },
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                    height=42,
                ),
            ),
        ],
    )

    def update_pagination_controls(page_buttons_container, page_info_text, prev_button, next_button):
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])
        page_info_text.value = f"Page {current_page['value']} of {total_pages} ({total_items['value']} total items)"
        page_info_text.update()

        prev_button.disabled = current_page["value"] <= 1
        next_button.disabled = current_page["value"] >= total_pages
        prev_button.update()
        next_button.update()

        page_buttons_container.controls.clear()
        start_page = max(1, current_page["value"] - 2)
        end_page = min(total_pages, start_page + 4)
        if start_page > 1:
            page_buttons_container.controls.append(
                ft.TextButton("1", on_click=lambda e: go_to_page(1), style=ft.ButtonStyle(color=s.COLOR_PRIMARY))
            )
            if start_page > 2:
                page_buttons_container.controls.append(ft.Text("..."))

        for page_num in range(start_page, end_page + 1):
            is_current = page_num == current_page["value"]
            page_buttons_container.controls.append(
                ft.TextButton(
                    str(page_num),
                    on_click=lambda e, p=page_num: go_to_page(p),
                    style=ft.ButtonStyle(
                        bgcolor=s.COLOR_PRIMARY if is_current else ft.Colors.TRANSPARENT,
                    ),
                )
            )
        if end_page < total_pages:
            if end_page < total_pages - 1:
                page_buttons_container.controls.append(ft.Text("..."))
            page_buttons_container.controls.append(
                ft.TextButton(str(total_pages), on_click=lambda e: go_to_page(total_pages), style=ft.ButtonStyle(color=s.COLOR_PRIMARY))
            )
        page_buttons_container.update()

    def go_to_page(page_num):
        current_page["value"] = page_num
        loadTable(searchInput.value or "", statusInput.value or "", page_num, items_per_page["value"])

    def change_items_per_page(e):
        items_per_page["value"] = int(e.control.value)
        current_page["value"] = 1
        loadTable(searchInput.value or "", statusInput.value or "", 1, items_per_page["value"])

    def go_to_previous_page(e):
        if current_page["value"] > 1:
            go_to_page(current_page["value"] - 1)

    def go_to_next_page(e):
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])
        if current_page["value"] < total_pages:
            go_to_page(current_page["value"] + 1)

    items_per_page_dropdown = ft.Dropdown(
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
        on_select=change_items_per_page,
        content_padding=ft.Padding.symmetric(horizontal=8, vertical=0),
    )

    prev_button = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        icon_color=s.COLOR_PRIMARY,
        on_click=go_to_previous_page,
        disabled=True,
        tooltip="Previous page",
    )

    next_button = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        icon_color=s.COLOR_PRIMARY,
        on_click=go_to_next_page,
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
                items_per_page_dropdown,
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

    table = ft.DataTable(
        border=ft.border.all(1, s.COLOR_BORDER),
        border_radius=12,
        horizontal_lines=ft.BorderSide(1, s.COLOR_BORDER),
        vertical_lines=ft.BorderSide(1, s.COLOR_BORDER),
        heading_row_height=42,
        data_row_min_height=52,
        data_row_max_height=52,
        heading_row_color="#f4f7fb",
        data_text_style=s.TABLE_DATA_STYLE,
        columns=[
            ft.DataColumn(label=ft.Text("Reg. no.", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Plate no.", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Vehicle", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Owner", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Reg. date", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Expiry date", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Status", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Actions", style=s.TABLE_HEADER_STYLE)),
        ],
        rows=[],
    )

    def loadTable(search="", status="", page_num=1, per_page=10):
        nonlocal all_rows_data
        try:
            all_rows_data = registration_db.getRegistrations(search, status)
        except Exception as exc:
            print("loadTable error:", exc)
            all_rows_data = []
            page.snack_bar = ft.SnackBar(ft.Text(f"Database error: {exc}"))
            page.snack_bar.open = True
            page.update()
            return

        total_items["value"] = len(all_rows_data)
        start_idx = (page_num - 1) * per_page
        end_idx = min(start_idx + per_page, len(all_rows_data))
        page_rows = all_rows_data[start_idx:end_idx]

        table.rows.clear()
        for row in page_rows:
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row["reg_no"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["plate_no"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row.get("vehicle_name", ""), style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row.get("owner", ""), style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(format_date_value(row["reg_date"]), style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(format_date_value(row["expiry_date"]), style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["status"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.Button(
                                        content=ft.Text("Edit", color="white", size=12, weight=ft.FontWeight.W_700),
                                        on_click=lambda e, reg_no=row["reg_no"]: show_edit_form(reg_no),
                                        style=s.BLUE_BUTTON_STYLE,
                                        height=32,
                                    ),
                                    ft.Button(
                                        content=ft.Text("Delete", color="white", size=12, weight=ft.FontWeight.W_700),
                                        on_click=lambda e, reg_no=row["reg_no"]: deleteRegistration(reg_no),
                                        style=ft.ButtonStyle(
                                            bgcolor={ft.ControlState.DEFAULT: "#B42318", ft.ControlState.HOVERED: "#dc5b4a"},
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                        ),
                                        height=32,
                                    ),
                                ],
                                spacing=6,
                                tight=True,
                            )
                        ),
                    ]
                )
            )

        update_pagination_controls(page_buttons_container, page_info_text, prev_button, next_button)
        table.update()

    def deleteRegistration(reg_no):
        try:
            registration_db.deleteRegistration(reg_no)
            page.snack_bar = ft.SnackBar(ft.Text("Registration deleted successfully."))
            page.snack_bar.open = True
            loadTable(searchInput.value or "", statusInput.value or "", current_page["value"], items_per_page["value"])
            page.update()
        except Exception as exc:
            page.snack_bar = ft.SnackBar(ft.Text(f"Delete failed: {exc}"))
            page.snack_bar.open = True
            page.update()

    def saveDetails(e):
        try:
            clear_errors()

            reg_no = (fRegNo.value or "").strip()
            plate_no = (fPlateNo.value or "").strip()
            reg_date_raw = (fRegDate.date_field.value or "").strip()
            expiry_date_raw = (fExpiryDate.date_field.value or "").strip()
            status = (fStatus.value or "").strip()

            has_errors = False
            if not reg_no:
                fRegNo.error.value = "Registration number is required."
                has_errors = True
            if not plate_no:
                fPlateNo.error.value = "Plate number is required."
                has_errors = True
            if not reg_date_raw:
                fRegDate.error.value = "Registration date is required."
                has_errors = True
            if not expiry_date_raw:
                fExpiryDate.error.value = "Expiry date is required."
                has_errors = True
            if not status:
                fStatus.error.value = "Status is required."
                has_errors = True

            if has_errors:
                page.update()
                return

            try:
                reg_date = datetime.datetime.strptime(reg_date_raw, "%m/%d/%Y").date()
            except Exception:
                fRegDate.error.value = "Invalid date (mm/dd/yyyy)"
                page.update()
                return

            try:
                expiry_date = datetime.datetime.strptime(expiry_date_raw, "%m/%d/%Y").date()
            except Exception:
                fExpiryDate.error.value = "Invalid date (mm/dd/yyyy)"
                page.update()
                return

            if reg_date > datetime.date.today():
                fRegDate.error.value = "Registration date cannot be in the future."
                page.update()
                return

            if reg_date > expiry_date:
                fExpiryDate.error.value = "Expiry must be after registration date."
                page.update()
                return

            if not vehicle_db.getVehicle(plate_no):
                fPlateNo.error.value = "That plate number does not exist in vehicles."
                page.update()
                return

            existing_reg = registration_db.getRegistration(reg_no)
            existing_plate = registration_db.getRegistrationByPlate(plate_no)

            if editingRegNo["value"]:
                if reg_no != editingRegNo["value"] and existing_reg:
                    fRegNo.error.value = "Registration number already exists."
                    page.update()
                    return
                if existing_plate and existing_plate["reg_no"] != editingRegNo["value"]:
                    fPlateNo.error.value = "That vehicle already has a registration."
                    page.update()
                    return
            else:
                if existing_reg:
                    fRegNo.error.value = "Registration number already exists."
                    page.update()
                    return
                if existing_plate:
                    fPlateNo.error.value = "That vehicle already has a registration."
                    page.update()
                    return

            if expiry_date <= datetime.date.today():
                status = "Expired"
                fExpiryDate.error.value = "Registration already expired; status set to Expired."

            data = {
                "reg_no": reg_no,
                "plate_no": plate_no,
                "reg_date": reg_date,
                "expiry_date": expiry_date,
                "status": status,
            }

            if editingRegNo["value"]:
                registration_db.updateRegistration(editingRegNo["value"], data)
            else:
                registration_db.addRegistration(data)

            hide_form()
            loadTable(searchInput.value or "", statusInput.value or "", current_page["value"], items_per_page["value"])
            page.snack_bar = ft.SnackBar(ft.Text("Registration saved successfully."))
            page.snack_bar.open = True
            page.update()
        except Exception as exc:
            print("saveDetails error:", exc)
            page.snack_bar = ft.SnackBar(ft.Text(f"Save failed: {exc}"))
            page.snack_bar.open = True
            page.update()

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
                ft.Text("Registration details", style=s.SECTION_TITLE_STYLE),
                ft.ResponsiveRow(
                    columns=12,
                    run_spacing=10,
                    controls=[
                        labeled_field("Registration no.", fRegNo, col=4),
                        labeled_field("Vehicle (plate no.)", fPlateNo, col=4),
                        labeled_field("Registration date", fRegDate, col=4),
                        labeled_field("Expiry date", fExpiryDate, col=4),
                        labeled_field("Status", fStatus, col=4),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Button(
                            content=primary_action_label,
                            style=s.BLUE_BUTTON_STYLE,
                            on_click=saveDetails,
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
        border=ft.border.all(1, s.COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
        visible=False,
    )

    table_block = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Registration list", style=s.SECTION_TITLE_STYLE),
                        ft.Text(
                            "Manage registration records from this screen",
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
                        controls=[table],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    border_radius=12,
                ),
                pagination_controls,
            ],
            spacing=10,
        ),
        padding=ft.padding.all(16),
        border=ft.border.all(1, s.COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
    )

    main_content = ft.Container(
        content=ft.ListView(
            controls=[
                ft.Row([menu_button], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=6),
                ft.Text("Registration", style=s.TITLE_STYLE),
                filters_row,
                table_block,
                form_box,
            ],
            spacing=16,
            expand=True,
        ),
        padding=ft.Padding.symmetric(horizontal=40, vertical=30),
        expand=True,
    )

    page.add(
        ft.Stack(
            controls=[main_content, sidebar],
            expand=True,
        )
    )

    loadTable("", "", 1, items_per_page["value"])
