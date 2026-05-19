# bringing in flet and our navigation tools so we can build out the vehicle management screen
# we import all our custom styles from the vehicle_styles file to keep the code clean
import flet as ft
import vehicle_db
import db
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
    # basic setup for the base screen with our custom fonts and white background
    page.bgcolor = "white"
    page.padding = 0
    page.fonts = GOOGLE_FONTS

    def go_to(screen_main, keep_sidebar_open=False):
        # wiping the controls and switching modules while carrying over the sidebar state
        page.controls.clear()
        screen_main(page, sidebar_open=keep_sidebar_open)
        page.update()

    def go_to_sign_in():
        # standard exit logic to take the user back to sign in
        from sign_in import main as sign_in_main
        page.controls.clear()
        sign_in_main(page)
        page.update()

    def on_menu_item_click(item_name):
        # routing dispatcher for all items in our sidebar navigation
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
        # a helper function to build themed text fields so we don't have to keep repeating the styling
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
            content_padding=ft.Padding.symmetric(horizontal=14, vertical=0),
        )

    def dropdown_input(options: list[str]) -> ft.Dropdown:
        # setting up styled dropdowns with a fixed scroll height for better usability
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
            content_padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            text_size=14,
            menu_height=220,
            dense=True,
        )

    def labeled_field(label: str, control: ft.Control, col: int = 6) -> ft.Container:
        # adding labels on top of our inputs and placing them in our responsive grid
        controls = [ft.Text(label, style=LABEL_STYLE), control]
        # if the control has an attached error Text control, add it below the input
        err = getattr(control, "custom_error", None)
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

    def filterVehicles(e=None):
        search = search_input.value or ""
        v_type = type_dropdown.value or ""
        current_page["value"] = 1
        loadTable(search, v_type, 1, items_per_page["value"])

    # initializing the sidebar and setting this screen as active
    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Vehicle", is_open=sidebar_open)
    # the hamburger icon to slide the sidebar in and out
    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e: (toggle_sidebar(sidebar), page.update()),
    )

    # trackers for the form title and primary button text
    form_title = ft.Text("Add vehicle", style=SECTION_TITLE_STYLE)
    primary_action_label = ft.Text("Add", color="white", weight=ft.FontWeight.W_700)
    def show_add_form(e=None):
        # making the form visible and setting it up for a new entry
        form_title.value = "Add vehicle"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def toggle_add_form(e=None):
        # toggling form visibility based on whether it is already open for adding
        if form_box.visible and form_title.value == "Add vehicle":
            hide_edit_form()
            return
        show_add_form()
        addForm()

    def show_edit_form(e=None):
        # using the same form box but switching labels for edit mode
        form_title.value = "Edit vehicle"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def addForm(e=None):
        editingPlateNo["value"] = None
        fPlateNo.value = ""
        fEngineNo.value = ""
        fChassisNo.value = ""
        fVehicleType.value = "Private car"
        fMake.value = ""
        fModel.value = ""
        fYear.value = ""
        fColor.value = ""
        updateOwnerDropdown()
        form_title.value = "Add vehicle"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def hide_edit_form(e=None):
        form_box.visible = False
        page.update()

    search_input = text_input("Search by plate or engine no.")
    search_input.prefix_icon = ft.Icons.SEARCH
    
    type_dropdown = dropdown_input(["All types", "Private car", "Motorcycle", "PUV"])

    # the row containing our global search and filtering tools for the vehicle table
    filters_row = ft.ResponsiveRow(
        columns=12,
        run_spacing=10,
        controls=[
            ft.Container(
                col={"xs": 12, "md": 4},
                content=search_input,
            ),
            ft.Container(
                col={"xs": 12, "md": 2},
                content=type_dropdown,
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
                    on_click=filterVehicles,
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

    # pagination trackers for the data list
    current_page = {"value": 1}
    items_per_page = {"value": 10}
    total_items = {"value": 0}

    def loadTable(search="", v_type="", page=1, per_page=10):
        # picking which vehicle rows to show based on our page index
        all_matching = vehicle_db.getVehicles(search, v_type)
        total_items["value"] = len(all_matching)
        # math to get the start and end of our data slice
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, len(all_matching))
        page_rows = all_matching[start_idx:end_idx]
        # repopulating the table with our selected data
        table.rows.clear()
        for vehicle in page_rows:
            table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(vehicle["plate_no"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle.get("engine_no", ""), style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle.get("chassis_no", ""), style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle["make_model"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(str(vehicle["year"]), style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle["type"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle["owner"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(
                        ft.Row(controls=[
                            ft.Button(
                                content=ft.Text("Edit", color="white", size=12, weight=ft.FontWeight.W_700),
                                on_click=lambda e, p=vehicle["plate_no"]: editVehicle(p),
                                style=BLUE_BUTTON_STYLE,
                                height=32,
                            ),
                            ft.Button(
                                content=ft.Text("Delete", color="white", size=12, weight=ft.FontWeight.W_700),
                                on_click=lambda e, p=vehicle["plate_no"]: deleteVehicle(p),
                                style=DANGER_BUTTON_STYLE,
                                height=32,
                            ),
                        ], spacing=6, tight=True)
                    ),
                ])
            )
        update_pagination_controls()
        table.update()

    def update_pagination_controls():
        # figuring out the total page count and updating our position label
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])
        page_info_text.value = f"Page {current_page['value']} of {total_pages} ({total_items['value']} total items)"
        page_info_text.update()
        # disabling arrows if we are at the start or end of the list
        prev_button.disabled = current_page["value"] <= 1
        next_button.disabled = current_page["value"] >= total_pages
        prev_button.update()
        next_button.update()
        # rebuilding the numeric buttons at the bottom
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
                        # highlighting the button for our active page
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
        # when a specific page button is clicked we reload the table with that index
        current_page["value"] = page_num
        loadTable(search_input.value, type_dropdown.value, page_num, items_per_page["value"])

    def change_items_per_page(e):
        # user changed the page size so we reset back to page 1 to avoid showing an empty index
        items_per_page["value"] = int(e.control.value)
        current_page["value"] = 1  # Reset to first page
        loadTable(search_input.value, type_dropdown.value, 1, items_per_page["value"])

    def getFormData():
        return {
            "plate_no": fPlateNo.value or "",
            "engine_no": fEngineNo.value or "",
            "chassis_no": fChassisNo.value or "",
            "vehicle_type": fVehicleType.value or "",
            "make": fMake.value or "",
            "model": fModel.value or "",
            "year": fYear.value or "",
            "color": fColor.value or "",
            "owner_id": fOwner.value or "",
        }

    # use shared show_dialog(page, title, message)

    def saveDetails(e):
        try:
            data = getFormData()
            print("saveDetails called", data)

            # basic client-side validation
            errors: list[str] = []
            if not data["plate_no"].strip():
                errors.append("Plate number is required.")
            if not data["engine_no"].strip():
                errors.append("Engine number is required.")
            if not data["chassis_no"].strip():
                errors.append("Chassis number is required.")
            if not data["make"].strip():
                errors.append("Make is required.")
            if not data["model"].strip():
                errors.append("Model is required.")
            if not data["owner_id"].strip():
                errors.append("Registered owner is required.")

            # validate year is an integer and plausible
            year_val = 0
            if data["year"] != "":
                try:
                    year_val = int(data["year"])
                    if year_val <= 0 or year_val > 9999:
                        errors.append("Year must be a positive integer.")
                except Exception:
                    errors.append("Year must be a number.")
            else:
                errors.append("Year is required.")

            # clear previous error messages
            for c in (fPlateNo, fEngineNo, fChassisNo, fMake, fModel, fYear, fOwner):
                try:
                    if getattr(c, "custom_error", None) is not None:
                        c.custom_error.value = ""
                except Exception:
                    pass

            if errors:
                # set inline error messages for the first failing fields
                if not data["plate_no"].strip():
                    fPlateNo.custom_error.value = "Plate number is required."
                if not data["engine_no"].strip():
                    fEngineNo.custom_error.value = "Engine number is required."
                if not data["chassis_no"].strip():
                    fChassisNo.custom_error.value = "Chassis number is required."
                if not data["make"].strip():
                    fMake.custom_error.value = "Make is required."
                if not data["model"].strip():
                    fModel.custom_error.value = "Model is required."
                if not data["owner_id"].strip():
                    fOwner.custom_error.value = "Registered owner is required."
                if data["year"] == "":
                    fYear.custom_error.value = "Year is required."
                page.update()
                return

            # normalize the year value before saving
            data["year"] = year_val

            # duplicate checks
            existing = vehicle_db.getVehicle(data["plate_no"]) if data["plate_no"] else None
            if editingPlateNo["value"]:
                # if changing plate no to another existing plate -> error
                if data["plate_no"] != editingPlateNo["value"] and existing:
                    fPlateNo.custom_error.value = "A vehicle with that plate number already exists."
                    page.update()
                    return
            else:
                if existing:
                    fPlateNo.custom_error.value = "A vehicle with that plate number already exists."
                    page.update()
                    return

            try:
                if editingPlateNo["value"]:
                    vehicle_db.updateVehicle(editingPlateNo["value"], data)
                else:
                    vehicle_db.addVehicle(data)
                hide_edit_form()
                loadTable(search_input.value, type_dropdown.value, current_page["value"], items_per_page["value"])
                page.snack_bar = ft.SnackBar(ft.Text("Vehicle saved successfully."))
                page.snack_bar.open = True
                page.update()
            except Exception as ex:
                # show friendly error to user and log to console
                page.snack_bar = ft.SnackBar(ft.Text(str(ex)))
                page.snack_bar.open = True
                page.update()
                print("DB error:", ex)
        except Exception as ex:
            print("saveDetails unexpected error:", ex)
            page.snack_bar = ft.SnackBar(ft.Text(str(ex)))
            page.snack_bar.open = True
            page.update()

    def editVehicle(plate_no):
        row = vehicle_db.getVehicle(plate_no)
        if not row: return
        editingPlateNo["value"] = plate_no
        fPlateNo.value = row["plate_no"]
        fEngineNo.value = row["engine_no"]
        fChassisNo.value = row["chassis_no"]
        fVehicleType.value = row["vehicle_type"]
        fMake.value = row["make"]
        fModel.value = row["model"]
        fYear.value = str(row["year"])
        fColor.value = row["color"]
        updateOwnerDropdown()
        fOwner.value = row["owner_id"]
        show_edit_form()

    def deleteVehicle(plate_no):
        vehicle_db.deleteVehicle(plate_no)
        loadTable(search_input.value, type_dropdown.value, current_page["value"], items_per_page["value"])

    def updateOwnerDropdown():
        drivers = db.getDrivers()
        fOwner.options = [ft.DropdownOption(key=d["license_no"], text=f"{d['full_name']} ({d['license_no']})") for d in drivers]
        if drivers:
            fOwner.value = drivers[0]["license_no"]
        fOwner.update()

    fPlateNo = text_input("e.g. ABC 1234")
    fPlateNo.custom_error = ft.Text("", color="red", size=12)
    fEngineNo = text_input("")
    fEngineNo.custom_error = ft.Text("", color="red", size=12)
    fChassisNo = text_input("")
    fChassisNo.custom_error = ft.Text("", color="red", size=12)
    fVehicleType = dropdown_input(["Motorcycle", "Private car", "PUV"])
    fMake = text_input("e.g. Toyota")
    fMake.custom_error = ft.Text("", color="red", size=12)
    fModel = text_input("e.g. Vios")
    fModel.custom_error = ft.Text("", color="red", size=12)
    fYear = text_input("e.g. 2020")
    fYear.custom_error = ft.Text("", color="red", size=12)
    fColor = text_input("e.g. White")
    fOwner = dropdown_input([])
    fOwner.custom_error = ft.Text("", color="red", size=12)
    editingPlateNo = {"value": None}

    def go_to_previous_page(e):
        # simple decrement of the page counter
        if current_page["value"] > 1:
            go_to_page(current_page["value"] - 1)

    def go_to_next_page(e):
        # simple increment of the page counter with a safety check against the max page
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])
        if current_page["value"] < total_pages:
            go_to_page(current_page["value"] + 1)

    # defining the table structure including its headers and borders
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
            ft.DataColumn(label=ft.Text("Engine no.", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Chassis no.", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Make / model", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Year", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Type", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Owner", style=TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Actions", style=TABLE_HEADER_STYLE)),
        ],
        rows=[],
    )

    items_per_page_dropdown = ft.Dropdown(
        # control for picking how many records are shown at a time
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

    # back button icon
    prev_button = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        icon_color=COLOR_PRIMARY,
        on_click=go_to_previous_page,
        disabled=True,
        tooltip="Previous page"
    )

    # forward button icon
    next_button = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        icon_color=COLOR_PRIMARY,
        on_click=go_to_next_page,
        disabled=True,
        tooltip="Next page"
    )
    # container for the dynamic page number buttons
    page_buttons_container = ft.Row(spacing=4, tight=True)
    page_info_text = ft.Text(
        "Page 1 of 1 (0 total items)",
        size=12,
        color=COLOR_TEXT_HINT,
        font_family="Lato"
    )
    pagination_controls = ft.Container(
        # assembly for the pagination control bar at the bottom
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
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        border=ft.border.all(1, COLOR_BORDER),
        border_radius=8,
        bgcolor="#f8f9fa",
    )
    table_block = ft.Container(
        # wrapping the table and title in a styled block
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
                pagination_controls,
            ],
            spacing=10,
        ),
        padding=ft.Padding.all(16),
        border=ft.border.all(1, COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
    )
    form_box = ft.Container(
        # the hidden container used for our data entry form
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
                    # grid layout for all our vehicle form fields
                    columns=12,
                    run_spacing=10,
                    controls=[
                        labeled_field("Plate number", fPlateNo, col=4),
                        labeled_field("Engine number", fEngineNo, col=4),
                        labeled_field("Chassis number", fChassisNo, col=4),
                        labeled_field("Vehicle type", fVehicleType, col=4),
                        labeled_field("Make", fMake, col=4),
                        labeled_field("Model", fModel, col=4),
                        labeled_field("Year", fYear, col=4),
                        labeled_field("Color", fColor, col=4),
                        labeled_field("Registered owner", fOwner, col=4),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Button(
                            content=primary_action_label,
                            style=BLUE_BUTTON_STYLE,
                            on_click=saveDetails,
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
        padding=ft.Padding.all(16),
        border=ft.border.all(1, COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
        visible=False,
    )
    main_content = ft.Container(
        # master layout for the vehicle screen
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
        padding=ft.Padding.symmetric(horizontal=40, vertical=30),
        expand=True,
    )
    # stacking the sidebar over our main content
    page.add(
        ft.Stack(
            controls=[
                main_content,
                sidebar,
            ],
            expand=True,
        )
    )

    # trigger the table load once the screen mounts
    loadTable(page=1, per_page=10)
