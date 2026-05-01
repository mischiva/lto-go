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

    # Sample vehicle data (replace with database calls when available)
    sample_vehicle_data = [
        {"plate_no": "ABC 1234", "make_model": "Toyota Vios", "year": "2020", "type": "Private car", "owner": "Juan Dela Cruz"},
        {"plate_no": "XYZ 5678", "make_model": "Honda Civic", "year": "2019", "type": "Private car", "owner": "Maria Santos"},
        {"plate_no": "DEF 9012", "make_model": "Ford Ranger", "year": "2021", "type": "Pickup truck", "owner": "Pedro Reyes"},
        {"plate_no": "GHI 3456", "make_model": "Mitsubishi Montero", "year": "2018", "type": "SUV", "owner": "Ana Garcia"},
        {"plate_no": "JKL 7890", "make_model": "Hyundai Tucson", "year": "2022", "type": "SUV", "owner": "Carlos Mendoza"},
        {"plate_no": "MNO 1357", "make_model": "Nissan Navara", "year": "2020", "type": "Pickup truck", "owner": "Rosa Lim"},
        {"plate_no": "PQR 2468", "make_model": "Toyota Fortuner", "year": "2019", "type": "SUV", "owner": "Miguel Torres"},
        {"plate_no": "STU 3690", "make_model": "Honda CR-V", "year": "2021", "type": "SUV", "owner": "Elena Cruz"},
        {"plate_no": "VWX 4812", "make_model": "Ford Everest", "year": "2017", "type": "SUV", "owner": "Roberto Diaz"},
        {"plate_no": "YZA 5924", "make_model": "Mitsubishi Strada", "year": "2018", "type": "Pickup truck", "owner": "Lourdes Ramos"},
        {"plate_no": "BCD 6035", "make_model": "Toyota Hilux", "year": "2022", "type": "Pickup truck", "owner": "Fernando Reyes"},
        {"plate_no": "EFG 7146", "make_model": "Honda City", "year": "2020", "type": "Sedan", "owner": "Carmen Flores"},
        {"plate_no": "HIJ 8257", "make_model": "Nissan Patrol", "year": "2016", "type": "SUV", "owner": "Antonio Valdez"},
        {"plate_no": "KLM 9368", "make_model": "Hyundai Santa Fe", "year": "2019", "type": "SUV", "owner": "Gloria Santos"},
        {"plate_no": "NOP 0479", "make_model": "Ford Focus", "year": "2018", "type": "Sedan", "owner": "Ricardo Moreno"},
    ]

    # Pagination state variables
    current_page = {"value": 1}
    items_per_page = {"value": 10}
    total_items = {"value": len(sample_vehicle_data)}
    all_rows_data = sample_vehicle_data.copy()  # Store all data for pagination

    def loadTable(page=1, per_page=10):
        """
        Load and display vehicle table data with pagination support.
        Currently uses sample data - replace with database calls when available.
        """
        # Sample vehicle data (replace with database query later)
        sample_vehicles = [
            {"plate_no": "ABC 1234", "make_model": "Toyota Vios", "year": "2020", "type": "Private car", "owner": "Juan Dela Cruz"},
            {"plate_no": "XYZ 5678", "make_model": "Honda Civic", "year": "2019", "type": "Private car", "owner": "Maria Santos"},
            {"plate_no": "DEF 9012", "make_model": "Ford Ranger", "year": "2021", "type": "Pickup truck", "owner": "Pedro Reyes"},
            {"plate_no": "GHI 3456", "make_model": "Mitsubishi Montero", "year": "2018", "type": "SUV", "owner": "Ana Garcia"},
            {"plate_no": "JKL 7890", "make_model": "Hyundai Tucson", "year": "2022", "type": "SUV", "owner": "Carlos Mendoza"},
            {"plate_no": "MNO 1357", "make_model": "Nissan Navara", "year": "2020", "type": "Pickup truck", "owner": "Rosa Flores"},
            {"plate_no": "PQR 2468", "make_model": "Toyota Fortuner", "year": "2019", "type": "SUV", "owner": "Miguel Torres"},
            {"plate_no": "STU 3690", "make_model": "Honda CR-V", "year": "2021", "type": "SUV", "owner": "Elena Castillo"},
            {"plate_no": "VWX 4826", "make_model": "Ford Everest", "year": "2020", "type": "SUV", "owner": "Roberto Silva"},
            {"plate_no": "YZA 5173", "make_model": "Mitsubishi Strada", "year": "2018", "type": "Pickup truck", "owner": "Lourdes Rivera"},
            {"plate_no": "BCD 6249", "make_model": "Toyota Hilux", "year": "2022", "type": "Pickup truck", "owner": "Fernando Lopez"},
            {"plate_no": "EFG 7381", "make_model": "Nissan Patrol", "year": "2019", "type": "SUV", "owner": "Carmen Morales"},
        ]

        # Update total items count
        total_items["value"] = len(sample_vehicles)

        # Calculate pagination bounds
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, len(sample_vehicles))
        page_rows = sample_vehicles[start_idx:end_idx]

        # Clear and populate table with current page data
        table.rows.clear()
        for vehicle in page_rows:
            table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(vehicle["plate_no"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle["make_model"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle["year"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle["type"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(ft.Text(vehicle["owner"], style=TABLE_DATA_STYLE)),
                    ft.DataCell(
                        ft.Row(controls=[
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
        loadTable(page_num, items_per_page["value"])

    def change_items_per_page(e):
        """Handle items per page change"""
        items_per_page["value"] = int(e.control.value)
        current_page["value"] = 1  # Reset to first page
        loadTable(1, items_per_page["value"])

    def go_to_previous_page(e):
        """Navigate to previous page"""
        if current_page["value"] > 1:
            go_to_page(current_page["value"] - 1)

    def go_to_next_page(e):
        """Navigate to next page"""
        total_pages = max(1, (total_items["value"] + items_per_page["value"] - 1) // items_per_page["value"])
        if current_page["value"] < total_pages:
            go_to_page(current_page["value"] + 1)

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
        rows=[],  # Will be populated by loadTable()
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
                pagination_controls,  # Add pagination controls below the table
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

    # Initial load of table data
    loadTable(1, 10)
