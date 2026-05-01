# Import the standard datetime module for handling date picker logic
import datetime
# Import the Flet framework for building the UI
import flet as ft
# Import sidebar logic for navigation and visibility toggling
from sidebar import build_sidebar, toggle_sidebar
# Import the shared font mapping for typography
from styles.fonts import GOOGLE_FONTS
# Import the specialized styling module for the Registration page
from styles import registration_styles as s


# Main entry point for the Registration module
def main(page: ft.Page, sidebar_open=False):
    # Initialize page-level styles based on the externalized style module
    page.bgcolor = "white"
    page.padding = 0
    page.fonts = GOOGLE_FONTS

    # Standard navigation dispatcher to clean the page and mount the next module
    def go_to(screen_main, keep_sidebar_open=False):
        page.controls.clear()
        screen_main(page, sidebar_open=keep_sidebar_open)
        page.update()

    # Redirects to the login screen, effectively ending the current session
    def go_to_sign_in():
        from sign_in import main as sign_in_main
        page.controls.clear()
        sign_in_main(page)
        page.update()

    # Handles click events from the sidebar menu items
    def on_menu_item_click(item_name):
        # Specific logic for toggling sidebar vs navigating
        if item_name == "__close__":
            toggle_sidebar(sidebar)
            return
        if item_name == "Sign out":
            go_to_sign_in()
            return

        # Route mappings based on the menu item name
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
        # helper to create uniform text fields for registration forms
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
        # building dropdowns that match our design system colors
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

    # pointer for the active field when using the date picker
    active_date_field = {"target": None}

    def on_date_change(e: ft.Event[ft.DatePicker]):
        # handling the value change when a user picks a date from the popup
        target = active_date_field["target"]
        if target and e.control.value:
            target.value = e.control.value.strftime("%m/%d/%Y")
            target.update()

    date_picker = ft.DatePicker(
        # setting up the system wide calendar range
        first_date=datetime.datetime(year=1900, month=1, day=1),
        last_date=datetime.datetime(year=2100, month=12, day=31),
        on_change=on_date_change,
    )
    page.overlay.append(date_picker)

    def date_input(hint_text: str) -> ft.Row:
        # pairing a locked text field with a calendar icon to handle dates
        date_field = text_input(hint_text)
        date_field.read_only = True
        def open_picker(e):
            # showing the calendar dialog and linking it to our field
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
        # adding labels on top of input controls for better readability
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

    # building the sidebar and marking registration as active
    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Registration", is_open=sidebar_open)

    # header menu icon button
    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e: (toggle_sidebar(sidebar), page.update()),
    )

    form_title = ft.Text("Add registration", style=s.SECTION_TITLE_STYLE)
    primary_action_label = ft.Text("Save", color="white", weight=ft.FontWeight.W_700)

    def show_add_form(e=None):
        # making the form visible for new entries
        form_title.value = "Add registration"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def show_edit_form(e=None):
        # switching to edit mode labels and showing the form
        form_title.value = "Edit registration"
        primary_action_label.value = "Save"
        form_box.visible = True
        page.update()

    def toggle_add_form(e=None):
        # switching form visibility based on its current state
        if form_box.visible and form_title.value == "Add registration":
            hide_form()
            return
        show_add_form()

    def hide_form(e=None):
        # closing the form and refreshing the ui
        form_box.visible = False
        page.update()

    # Responsive row containing search and filter controls for the registration list
    filters_row = ft.ResponsiveRow(
        columns=12,
        run_spacing=10,
        controls=[
            ft.Container(
                col={"xs": 12, "md": 4},
                content=ft.TextField(
                    hint_text="Search by reg. no. or plate",
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
                    "All statuses",
                    "Active",
                    "Expired",
                    "Suspended",
                ]),
            ),
            ft.Container(col={"xs": 0, "md": 3}),
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
                        "+ New registration",
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

    sample_registration_data = [
        # temporary list for building out the table logic
        {"reg_no": "REG-2025-001", "plate_no": "ABC 1234", "reg_date": "2025-01-10", "expiry_date": "2026-01-10", "status": "Active"},
        {"reg_no": "REG-2025-002", "plate_no": "XYZ 5678", "reg_date": "2025-02-15", "expiry_date": "2026-02-15", "status": "Active"},
        {"reg_no": "REG-2025-003", "plate_no": "DEF 9012", "reg_date": "2025-03-05", "expiry_date": "2026-03-05", "status": "Expired"},
        {"reg_no": "REG-2025-004", "plate_no": "GHI 3456", "reg_date": "2025-04-12", "expiry_date": "2026-04-12", "status": "Suspended"},
        {"reg_no": "REG-2025-005", "plate_no": "JKL 7890", "reg_date": "2025-05-20", "expiry_date": "2026-05-20", "status": "Active"},
        {"reg_no": "REG-2025-006", "plate_no": "MNO 1357", "reg_date": "2025-06-30", "expiry_date": "2026-06-30", "status": "Expired"},
        {"reg_no": "REG-2025-007", "plate_no": "PQR 2468", "reg_date": "2025-07-11", "expiry_date": "2026-07-11", "status": "Active"},
        {"reg_no": "REG-2025-008", "plate_no": "STU 3690", "reg_date": "2025-08-02", "expiry_date": "2026-08-02", "status": "Suspended"},
        {"reg_no": "REG-2025-009", "plate_no": "VWX 4812", "reg_date": "2025-09-18", "expiry_date": "2026-09-18", "status": "Active"},
        {"reg_no": "REG-2025-010", "plate_no": "YZA 5924", "reg_date": "2025-10-25", "expiry_date": "2026-10-25", "status": "Active"},
        {"reg_no": "REG-2025-011", "plate_no": "BCD 6035", "reg_date": "2025-11-07", "expiry_date": "2026-11-07", "status": "Expired"},
        {"reg_no": "REG-2025-012", "plate_no": "EFG 7146", "reg_date": "2025-12-14", "expiry_date": "2026-12-14", "status": "Active"},
    ]

    # state trackers for our list pagination
    current_page = {"value": 1}
    items_per_page = {"value": 10}
    total_items = {"value": len(sample_registration_data)}
    all_rows_data = sample_registration_data.copy()

    # defining the columns and visual style of our registration table
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
            ft.DataColumn(label=ft.Text("Reg. date", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Expiry date", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Status", style=s.TABLE_HEADER_STYLE)),
            ft.DataColumn(label=ft.Text("Actions", style=s.TABLE_HEADER_STYLE)),
        ],
        rows=[],
    )

    def loadTable(page=1, per_page=10):
        # picking which rows to show based on the current page index
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
                        ft.DataCell(ft.Text(row["reg_no"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["plate_no"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["reg_date"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["expiry_date"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(ft.Text(row["status"], style=s.TABLE_DATA_STYLE)),
                        ft.DataCell(
                            ft.Row(controls=[
                                ft.Button(
                                    # EDIT
                                    content=ft.Text("Edit", color="white", size=12, weight=ft.FontWeight.W_700),
                                    on_click=show_edit_form,
                                    style=s.BLUE_BUTTON_STYLE,
                                    height=32,
                                ),
                                ft.Button(
                                    # DELETE
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
        # recalculating the total pages and updating the position label
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

    # Action for back button
    def go_to_previous_page(e):
        if current_page["value"] > 1:
            go_to_page(current_page["value"] - 1)

    # Action for forward button
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
        # assembling the pagination strip at the bottom of the table
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
        # wrapping the table and title section in a styled container
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Registration list", style=s.SECTION_TITLE_STYLE),
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
                        form_title, # Dynamic header
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
                        labeled_field("Vehicle (plate no.)", text_input("e.g. ABC 1234"), col=4),
                        labeled_field("Registration date", date_input("mm/dd/yyyy"), col=4),
                        labeled_field("Expiry date", date_input("mm/dd/yyyy"), col=4),
                        labeled_field("Status", dropdown_input(["Active", "Expired", "Suspended"]), col=4),
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
                ft.Text("Registration", style=s.TITLE_STYLE),
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

    # loading the initial data set when the screen first opens
    loadTable(1, items_per_page["value"])
