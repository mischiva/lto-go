import flet as ft
import datetime
import db
from sidebar import build_sidebar, toggle_sidebar
from styles.fonts import GOOGLE_FONTS
from styles.driver_styles import (
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
            page.update()
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
                    icon_color=COLOR_PRIMARY,
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
                    ft.Text(label, style=LABEL_STYLE),
                    control,
                ],
                spacing=6,
                tight=True,
            ),
        )

    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Driver", is_open=sidebar_open)

    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e: (toggle_sidebar(sidebar), page.update()),
    )

    form_title = ft.Text("Add driver", style=SECTION_TITLE_STYLE)
    primary_action_label = ft.Text("Save", color="white", weight=ft.FontWeight.W_700)

    def addForm(e=None):
        editingLicenseNo["value"] = None

        # clear all fields
        fLastName.value      = ""
        fFirstName.value     = ""
        fMiddleName.value    = ""
        fSuffix.value        = ""
        fLicenseNo.value     = ""
        fSex.value           = "M - Male"
        fLicenseType.value   = "Non-Professional"
        fLicenseStatus.value = "Valid"
        fDob.controls[0].content.value           = ""
        fLicenseIssued.controls[0].content.value = ""
        fLicenseExpiry.controls[0].content.value = ""

        form_title.value = "Add driver"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def toggle_add_form(e=None):
        if form_box.visible and form_title.value == "Add driver":
            hide_edit_form()
            return
        addForm()

    def editForm(): # just shows the edit form, nothing else
        form_title.value = "Edit driver"
        primary_action_label.value = "Update"
        form_box.visible = True
        page.update()

    def hide_edit_form(e=None):
        form_box.visible = False
        page.update()

    # Pagination state variables
    current_page = {"value": 1}
    items_per_page = {"value": 10}
    total_items = {"value": 0}
    all_rows_data = []  # Store all data for pagination

    def loadTable(search="", license_type="", license_status="", sex="", page=1, per_page=10):
        # Get all matching rows from database
        all_matching_rows = db.getDrivers(search, license_type, license_status, sex)
        total_items["value"] = len(all_matching_rows)
        all_rows_data.clear()
        all_rows_data.extend(all_matching_rows)

        # Calculate pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_rows = all_matching_rows[start_idx:end_idx]

        # Clear and populate table with current page data
        table.rows.clear()
        for r in page_rows:
            license_no   = r["license_no"]
            full_name    = r["full_name"]
            dob          = str(r["dob"])
            age          = str(r["age"])
            sex_val      = r["sex"].strip()
            ltype        = r["license_type"]
            lstatus      = r["license_status"]
            expires      = str(r["license_expire"])
            type_display = {"Non-Professional": "NP", "Professional": "P", "Student": "SP"}.get(ltype, ltype)
            table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(license_no,   style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(full_name,    style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(dob,          style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(age,          style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(sex_val,      style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(type_display, style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(lstatus,      style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(expires,      style=TABLE_DATA_STYLE)),
                    ft.DataCell(
                        ft.Row(controls=[
                            ft.Button(
                                content=ft.Text("Edit", color="white", size=12, weight=ft.FontWeight.W_700),
                                on_click=lambda e, ln=license_no: editDriver(ln),
                                style=BLUE_BUTTON_STYLE,
                                height=32,
                            ),
                            ft.Button(
                                content=ft.Text("Delete", color="white", size=12, weight=ft.FontWeight.W_700),
                                on_click=lambda e, ln=license_no: deleteDriver(ln),
                                style=DANGER_BUTTON_STYLE,
                                height=32,
                            ),
                        ], spacing=6, tight=True)
                    ),
                ])
            )

        # Update pagination controls
        update_pagination_controls()
        table.update()

    def update_pagination_controls():
        """Update pagination UI elements based on current state"""
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])

        # Update page info text
        page_info_text.value = f"Page {current_page['value']} of {total_pages} ({total_items['value']} total items)"
        page_info_text.update()

        # Update navigation buttons
        prev_button.disabled = current_page["value"] <= 1
        next_button.disabled = current_page["value"] >= total_pages
        prev_button.update()
        next_button.update()

        # Update page number buttons
        page_buttons_container.controls.clear()
        start_page = max(1, current_page["value"] - 2)
        end_page = min(total_pages, start_page + 4)

        if start_page > 1:
            page_buttons_container.controls.append(
                ft.TextButton("1", on_click=lambda e: go_to_page(1), style=ft.ButtonStyle(color=COLOR_PRIMARY))
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
                        color=COLOR_PRIMARY if not is_current else "white",
                        bgcolor=COLOR_PRIMARY if is_current else ft.Colors.TRANSPARENT
                    )
                )
            )

        if end_page < total_pages:
            if end_page < total_pages - 1:
                page_buttons_container.controls.append(ft.Text("..."))
            page_buttons_container.controls.append(
                ft.TextButton(str(total_pages), on_click=lambda e: go_to_page(total_pages), style=ft.ButtonStyle(color=COLOR_PRIMARY))
            )

        page_buttons_container.update()

    def go_to_page(page_num):
        """Navigate to a specific page"""
        current_page["value"] = page_num
        loadTable(
            searchInput.value or "",
            typeMap.get(typeInput.value, ""),
            licenseStatusMap.get(statusInput.value, ""),
            sexMap.get(sexInput.value, ""),
            page_num,
            items_per_page["value"]
        )

    def change_items_per_page(e):
        """Handle items per page change"""
        items_per_page["value"] = int(e.control.value)
        current_page["value"] = 1  # Reset to first page
        loadTable(
            searchInput.value or "",
            typeMap.get(typeInput.value, ""),
            licenseStatusMap.get(statusInput.value, ""),
            sexMap.get(sexInput.value, ""),
            1,
            items_per_page["value"]
        )

    def go_to_previous_page(e):
        """Navigate to previous page"""
        if current_page["value"] > 1:
            go_to_page(current_page["value"] - 1)

    def go_to_next_page(e):
        """Navigate to next page"""
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])
        if current_page["value"] < total_pages:
            go_to_page(current_page["value"] + 1)

    def getFormData():
        # date_input returns a Row — the actual TextField is inside controls[0].content
        def getDate(dateRow):
            return dateRow.controls[0].content.value or ""

        # sex dropdown shows "M - Male" but db only needs "M"
        def getSex(dropdown):
            return dropdown.value.split(" - ")[0] if dropdown.value else ""

        return {
            "license_no":     fLicenseNo.value or "",
            "last_name":      fLastName.value or "",
            "first_name":     fFirstName.value or "",
            "middle_name":    fMiddleName.value or None,
            "suffix":         fSuffix.value or None,
            "dob":            getDate(fDob),
            "sex":            getSex(fSex),
            "license_type":   fLicenseType.value or "",
            "license_status": fLicenseStatus.value or "",
            "license_issued": getDate(fLicenseIssued),
            "license_expire": getDate(fLicenseExpiry),
        }

    def filterDrivers(e=None): # function that runs on click of filter button
        search = searchInput.value or "" # gets the value of the search input, or empty string if nothing is entered

        typeMap = { # since what's written is different from database format, this map is to ensure that it is the same
            "NP - Non-Professional": "Non-Professional",
            "P - Professional":"Professional",
            "SP - Student Permit":"Student",
        }
        sexMap = {
            "M": "M",
            "F": "F",
        }
        licenseStatusMap = {
            "Valid":     "Valid",
            "Expired":   "Expired",
            "Suspended": "Suspended",
            "Revoked":   "Revoked",
        }

        licenseType = typeMap.get(typeInput.value, "") # gets map, if not in map (for example, all licenses) returns an empty string
        sex = sexMap.get(sexInput.value, "")
        licenseStatus =licenseStatusMap.get(statusInput.value, "")

        # Reset to first page when filtering
        current_page["value"] = 1
        loadTable(search, licenseType, licenseStatus, sex, 1, items_per_page["value"]) # loads table again, but this time with updated filter parameters

    def saveDetails(e):
        data = getFormData()
        try:
            if editingLicenseNo["value"]:
                db.updateDriver(editingLicenseNo["value"], data)
            else:
                db.addDriver(data)
            hide_edit_form()
            # Reload current page after save
            loadTable(
                searchInput.value or "",
                typeMap.get(typeInput.value, ""),
                licenseStatusMap.get(statusInput.value, ""),
                sexMap.get(sexInput.value, ""),
                current_page["value"],
                items_per_page["value"]
            )
        except Exception as ex:
            print("DB error:", ex)

    def editDriver(license_no): # edit driver doesn't actually edit, instead shows the forms that the user can change when they want to edit the driver's details
        row = db.getDriver(license_no) # uses getDriver command from db.py to get the driver's details
        if not row:
            return
        editingLicenseNo["value"] = license_no
        fLastName.value = row["last_name"]
        fFirstName.value = row["first_name"]
        fMiddleName.value = row["middle_name"] or ""
        fSuffix.value = row["suffix"] or ""
        fLicenseNo.value = row["license_no"]
        fSex.value = "M - Male" if row["sex"].strip() == "M" else "F - Female"
        fLicenseType.value = row["license_type"]
        fLicenseStatus.value = row["license_status"]
        fDob.controls[0].content.value = str(row["dob"])
        fLicenseIssued.controls[0].content.value = str(row["license_issued"])
        fLicenseExpiry.controls[0].content.value = str(row["license_expire"])
        
        editForm()
        page.update()

    def deleteDriver(license_no):
        db.deleteDriver(license_no)
        # Reload table, adjusting page if necessary
        total_pages = max(1, (total_items["value"] - 1 + items_per_page["value"] - 1) // items_per_page["value"])
        if current_page["value"] > total_pages:
            current_page["value"] = max(1, total_pages)
        loadTable(
            searchInput.value or "",
            typeMap.get(typeInput.value, ""),
            licenseStatusMap.get(statusInput.value, ""),
            sexMap.get(sexInput.value, ""),
            current_page["value"],
            items_per_page["value"]
        )

    searchInput=ft.TextField(
        hint_text="Search by license no. or name",
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
    )
    
    typeInput=dropdown_input([
        "All license types",
        "NP - Non-Professional",
        "P - Professional",
        "SP - Student Permit",
    ])

    statusInput=dropdown_input([
        "All statuses",
        "Valid",
        "Expired",
        "Suspended",
        "Revoked",
    ])
    
    sexInput=dropdown_input([
        "All sex",
        "M",
        "F",
    ])

    typeMap = {
        "All license types": "",
        "NP - Non-Professional": "Non-Professional",
        "P - Professional": "Professional",
        "SP - Student Permit": "Student",
    }

    sexMap = {
        "All sex": "",
        "M": "M",
        "F": "F",
    }

    licenseStatusMap = {
        "All statuses": "",
        "Valid": "Valid",
        "Expired": "Expired",
        "Suspended": "Suspended",
        "Revoked": "Revoked",
    }

    filters_row = ft.ResponsiveRow(
        columns=12,
        run_spacing=10,
        controls=[
            ft.Container(
                col={"xs": 12, "md": 3},
                content=searchInput
            ),
            ft.Container(
                col={"xs": 12, "sm": 4, "md": 2},
                content=typeInput
            ),
            ft.Container(
                col={"xs": 12, "sm": 4, "md": 2},
                content=statusInput
            ),
            ft.Container(
                col={"xs": 12, "sm": 4, "md": 2},
                content=sexInput
            ),
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
                    on_click=filterDrivers,
                ),
            ),
            ft.Container(
                col={"xs": 6, "md": 2},
                content=ft.Button(
                    content=ft.Text(
                        "+ Add driver",
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

    # Pagination controls
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
        content_padding=ft.padding.symmetric(horizontal=8, vertical=0),
    )

    prev_button = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        icon_color=COLOR_PRIMARY,
        on_click=go_to_previous_page,
        disabled=True,
        tooltip="Previous page"
    )

    next_button = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        icon_color=COLOR_PRIMARY,
        on_click=go_to_next_page,
        disabled=True,
        tooltip="Next page"
    )

    page_buttons_container = ft.Row(spacing=4, tight=True)

    page_info_text = ft.Text(
        "Page 1 of 1 (0 total items)",
        size=12,
        color=COLOR_TEXT_HINT,
        font_family="Lato"
    )

    pagination_controls = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Show:", size=12, color=COLOR_TEXT_HINT, font_family="Lato"),
                items_per_page_dropdown,
                ft.Container(width=20),  # Spacer
                prev_button,
                page_buttons_container,
                next_button,
                ft.Container(width=20),  # Spacer
                page_info_text,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border=ft.border.all(1, COLOR_BORDER),
        border_radius=8,
        bgcolor="#f8f9fa",
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
            ft.DataColumn(label=ft.Text("License no.", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Name", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("DOB", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Age", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Sex", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Type", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Status", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Expires", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Actions", style=TABLE_HEADER_STYLE)),
        ],
        rows=[],
    )

    table_block = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Driver list", style=SECTION_TITLE_STYLE),
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
                pagination_controls,  # Add pagination controls below the table
            ],
            spacing=10,
        ),
        padding=ft.padding.all(16),
        border=ft.border.all(1, COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
    )

    # this field is for forms, we just assign them variable names so we can access it later on
    fLastName      = text_input("e.g. Dela Cruz") 
    fFirstName     = text_input("e.g. Juan")
    fMiddleName    = text_input("e.g. Magtanggol")
    fSuffix        = text_input("Jr., Sr., III")
    fLicenseNo     = text_input("A00-00-000000")
    fDob           = date_input("mm/dd/yyyy")
    fSex           = dropdown_input(["M - Male", "F - Female"])
    fLicenseType   = dropdown_input(["Non-Professional", "Professional", "Student"])
    fLicenseStatus = dropdown_input(["Valid", "Expired", "Suspended", "Revoked"])
    fLicenseIssued = date_input("mm/dd/yyyy")
    fLicenseExpiry = date_input("mm/dd/yyyy")

    editingLicenseNo = {"value": None}  # tracks which driver is being edited

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
                ft.Text(
                    "Complete all required details, then save.",
                    size=12,
                    color="#6b7280",
                    font_family="Lato",
                ),
                ft.Text("Driver details", style=SECTION_TITLE_STYLE),
                ft.ResponsiveRow(
                    columns=12,
                    run_spacing=10,
                    controls=[
                        labeled_field("Last name", fLastName, col=3),
                        labeled_field("First name", fFirstName, col=3),
                        labeled_field("Middle name", fMiddleName, col=3),
                        labeled_field("Suffix", fSuffix, col=3),
                        labeled_field("License no.", fLicenseNo, col=4),
                        labeled_field("Date of birth", fDob, col=4),
                        labeled_field("Sex", fSex, col=4),
                        labeled_field("License type", fLicenseType, col=4),
                        labeled_field("License status", fLicenseStatus, col=4),
                        labeled_field("License issued", fLicenseIssued, col=4),
                        labeled_field("License expiry", fLicenseExpiry, col=4),
                    ],
                ),
                ft.Text("Address", style=SECTION_TITLE_STYLE),
                ft.ResponsiveRow(
                    columns=12,
                    run_spacing=10,
                    controls=[
                        labeled_field("Street", text_input("e.g. 12 Rizal St."), col=6),
                        labeled_field("Barangay", text_input("e.g. Batong Malake"), col=6),
                        labeled_field("City / municipality", text_input("e.g. Los Banos"), col=6),
                        labeled_field("Region", text_input("e.g. Region IV-A"), col=6),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Button(
                            content=primary_action_label,
                            style=BLUE_BUTTON_STYLE,
                            on_click=saveDetails
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
                ft.Text("Driver", style=TITLE_STYLE),
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

    loadTable(page=1, per_page=10)  # Initial load with pagination
