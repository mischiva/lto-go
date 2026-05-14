# using standard date handling
import datetime
# standard flet import
import flet as ft
# getting our sidebar and styling tools
from sidebar import build_sidebar, toggle_sidebar
from styles.fonts import GOOGLE_FONTS
from styles import violation_styles as s


def main(page: ft.Page, sidebar_open=False):
    # basic page settings
    page.bgcolor = "white"
    page.padding = 0
    page.fonts = GOOGLE_FONTS

    def go_to(screen_main, keep_sidebar_open=False):
        # wiping the page and mounting the new screen while preserving the sidebar open state
        page.controls.clear()
        screen_main(page, sidebar_open=keep_sidebar_open)
        page.update()

    def go_to_sign_in():
        # logging the user out and showing the sign in hero
        from sign_in import main as sign_in_main
        page.controls.clear()
        sign_in_main(page)
        page.update()

    def on_menu_item_click(item_name):
        # logic for handling sidebar link clicks
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
        # helper to keep all our text fields styled identically
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
            content_padding=ft.padding.symmetric(horizontal=14, vertical=0),
        )

    def dropdown_input(options: list[str]) -> ft.Dropdown:
        # building dropdowns that match our brand blue and layout
        return ft.Dropdown(
            options=[ft.DropdownOption(key=opt, text=opt) for opt in options],
            value=options[0] if len(options) > 0 else None,
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
            content_padding=ft.padding.symmetric(horizontal=14, vertical=8),
            text_size=14,
            menu_height=220,
            dense=True,
        )

    # tracking which field should receive the input from the date picker
    active_date_field = {"target": None}

    def on_date_change(e: ft.Event[ft.DatePicker]):
        # updating the text value once the user picks a day from the calendar
        target = active_date_field["target"]
        if target and e.control.value:
            target.value = e.control.value.strftime("%m/%d/%Y")
            target.update()

    date_picker = ft.DatePicker(
        # setting up the calendar bounds
        first_date=datetime.datetime(year=1900, month=1, day=1),
        last_date=datetime.datetime(year=2100, month=12, day=31),
        on_change=on_date_change,
    )
    page.overlay.append(date_picker)

    def date_input(hint_text: str) -> ft.Row:
        # pairing a locked text input with a calendar icon
        date_field = text_input(hint_text)
        date_field.read_only = True
        def open_picker(e):
            # linking the picker to this field before showing the dialog
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

    def labeled_field(label: str, control: ft.Control, col: int = 6) -> ft.Container:
        # adding labels on top of form inputs for better readability
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

    # building the sidebar and marking violation as active
    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Violation", is_open=sidebar_open)

    # the hamburger icon for toggling the sidebar
    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e: (toggle_sidebar(sidebar), page.update()),
    )

    form_title = ft.Text("Add violation", style=s.SECTION_TITLE_STYLE)
    primary_action_label = ft.Text("Save", color="white", weight=ft.FontWeight.W_700)

    def show_add_form(e=None):
        # opening the form for a new entry
        form_title.value = "Add violation"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def toggle_add_form(e=None):
        if form_box.visible and form_title.value == "Add violation":
            hide_form()
            return
        show_add_form()

    def show_edit_form(e=None):
        # updating labels and showing the form for editing
        form_title.value = "Edit violation"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def hide_form(e=None):
        # hiding the form and updating ui
        form_box.visible = False
        page.update()

    # Row containing global search and status filters
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
            ft.Container(col={"xs": 0, "md": 1}),
            ft.Container(
                col={"xs": 6, "md": 1},
                content=ft.Button(
                    # FILTER BUTTON
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
                    style=s.BLUE_BUTTON_STYLE,
                    height=46,
                    width=float("inf"),
                    on_click=lambda e: None,
                ),
            ),
            ft.Container(
                col={"xs": 6, "md": 2},
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
                    style=s.BLUE_BUTTON_STYLE,
                    height=46,
                    width=float("inf"),
                    on_click=toggle_add_form,
                ),
            ),
        ],
    )

    sample_violation_data = [
        # temporary list for building the table and pagination logic
        {"driver": "Juan Dela Cruz", "plate_no": "ABC 1234", "type": "Overspeeding", "date": "2025-06-10", "location": "Calamba, Laguna", "fine": "2,000", "status": "Unpaid"},
        {"driver": "Maria Santos", "plate_no": "XYZ 5678", "type": "Reckless driving", "date": "2025-05-12", "location": "San Pablo, Laguna", "fine": "1,500", "status": "Paid"},
        {"driver": "Pedro Reyes", "plate_no": "DEF 9012", "type": "No seatbelt", "date": "2025-04-22", "location": "Sta. Rosa, Laguna", "fine": "500", "status": "Contested"},
        {"driver": "Ana Garcia", "plate_no": "GHI 3456", "type": "Overspeeding", "date": "2025-03-10", "location": "Binan, Laguna", "fine": "2,000", "status": "Paid"},
        {"driver": "Carlos Mendoza", "plate_no": "JKL 7890", "type": "Reckless driving", "date": "2025-02-14", "location": "Cabuyao, Laguna", "fine": "1,500", "status": "Unpaid"},
        {"driver": "Rosa Lim", "plate_no": "MNO 1357", "type": "No seatbelt", "date": "2025-01-18", "location": "Los Banos, Laguna", "fine": "500", "status": "Paid"},
        {"driver": "Miguel Torres", "plate_no": "PQR 2468", "type": "Overspeeding", "date": "2024-12-02", "location": "Calamba, Laguna", "fine": "2,000", "status": "Contested"},
        {"driver": "Elena Cruz", "plate_no": "STU 3690", "type": "Reckless driving", "date": "2024-11-07", "location": "San Pedro, Laguna", "fine": "1,500", "status": "Paid"},
        {"driver": "Roberto Diaz", "plate_no": "VWX 4812", "type": "No seatbelt", "date": "2024-10-25", "location": "Ibaan, Batangas", "fine": "500", "status": "Unpaid"},
        {"driver": "Lourdes Ramos", "plate_no": "YZA 5924", "type": "Overspeeding", "date": "2024-09-11", "location": "San Pablo, Laguna", "fine": "2,000", "status": "Paid"},
        {"driver": "Fernando Reyes", "plate_no": "BCD 6035", "type": "Reckless driving", "date": "2024-08-03", "location": "Sta. Rosa, Laguna", "fine": "1,500", "status": "Contested"},
        {"driver": "Carmen Flores", "plate_no": "EFG 7146", "type": "No seatbelt", "date": "2024-07-19", "location": "Biñan, Laguna", "fine": "500", "status": "Paid"},
    ]

    # state trackers for our list pagination
    current_page = {"value": 1}
    items_per_page = {"value": 10}
    total_items = {"value": len(sample_violation_data)}
    all_rows_data = sample_violation_data.copy()

    # defining the structure and look of our data table
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
            ft.DataColumn(label=ft.Text("Driver", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Plate no.", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Violation type", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Date", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Location", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Fine (PHP)", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Status", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Actions", style=s.TABLE_HEADER_STYLE)),
        ],
        rows=[],
    )

    def loadTable(page=1, per_page=10):
        # picking which slice of data to show based on the page index
        total_items["value"] = len(all_rows_data)
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, len(all_rows_data))
        page_rows = all_rows_data[start_idx:end_idx]
        # clearing the table and repopulating with the new slice
        table.rows.clear()
        for row in page_rows:
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row["driver"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["plate_no"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["type"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["date"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["location"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["fine"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["status"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(
                            ft.Row(controls=[
                                ft.Button(
                                    # EDIT BUTTON
                                    content=ft.Text("Edit", color="white", size=12, weight=ft.FontWeight.W_700),
                                    on_click=show_edit_form,
                                    style=s.BLUE_BUTTON_STYLE,
                                    height=32,
                                ),
                                ft.Button(
                                    #\\ DELETE BUTTON
                                    content=ft.Text("Delete", color="white", size=12, weight=ft.FontWeight.W_700),
                                    on_click=lambda e: None,
                                    style=ft.ButtonStyle(
                                        bgcolor={ft.ControlState.DEFAULT: "#B42318", ft.ControlState.HOVERED: "#dc5b4a"},
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                    ),
                                    height=32,
                                ),
                            ], spacing=6, tight=True)
                        ),
                    ]
                )
            )

        update_pagination_controls()
        table.update()

    def update_pagination_controls():
        # math to figure out how many pages we need and updating the label
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])
        page_info_text.value = f"Page {current_page['value']} of {total_pages} ({total_items['value']} total items)"
        page_info_text.update()

        prev_button.disabled = current_page["value"] <= 1
        next_button.disabled = current_page["value"] >= total_pages
        prev_button.update()
        next_button.update()
        # rebuilding the numeric buttons for navigation
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
                        # highlighting the active page button
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
        # switching to a specific page when clicked
        current_page["value"] = page_num
        loadTable(page_num, items_per_page["value"])

    def change_items_per_page(e):
        # resetting to page 1 after changing the rows per page limit
        items_per_page["value"] = int(e.control.value)
        current_page["value"] = 1
        loadTable(1, items_per_page["value"])

    # Back navigation
    def go_to_previous_page(e):
        if current_page["value"] > 1:
            go_to_page(current_page["value"] - 1)

    # Forward navigation
    def go_to_next_page(e):
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])
        if current_page["value"] < total_pages:
            go_to_page(current_page["value"] + 1)

    items_per_page_dropdown = ft.Dropdown(
        # selector for how many records are shown at once
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
        # assembly for the pagination bar at the bottom
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
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border=ft.border.all(1, s.COLOR_BORDER),
        border_radius=8,
        bgcolor="#f8f9fa",
    )

    table_block = ft.Container(
        # wrapping the table and header inside a styled container
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Violation list", style=s.SECTION_TITLE_STYLE),
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
        padding=ft.padding.all(16),
        border=ft.border.all(1, s.COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
    )

    form_box = ft.Container(
        # the hidden container used for creating or editing records
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        form_title, # Responsive heading
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
                ft.Text("Violation details", style=s.SECTION_TITLE_STYLE),
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
                            style=s.BLUE_BUTTON_STYLE,
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
        border=ft.border.all(1, s.COLOR_BORDER),
        border_radius=14,
        bgcolor="white",
        visible=False,
    )

    main_content = ft.Container(
        # the master scrolling container for the whole screen
        content=ft.ListView(
            controls=[
                ft.Row([menu_button], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=6),
                ft.Text("Violation", style=s.TITLE_STYLE),
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

    # loading the data set when the screen opens
    loadTable(1, items_per_page["value"])
