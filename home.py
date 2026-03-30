import flet as ft
from styles.fonts import GOOGLE_FONTS
from styles import home_styles as s
from sidebar import build_sidebar, toggle_sidebar
from driver import main as driver_main
from vehicle import main as vehicle_main
from registration import main as registration_main
from violation import main as violation_main
from reports import main as reports_main


def main(page: ft.Page, sidebar_open=False):
    # Page
    page.bgcolor = s.PAGE_BGCOLOR
    page.padding = s.PAGE_PADDING
    page.fonts = GOOGLE_FONTS

    # Navigation
    def go_to(screen_main, keep_sidebar_open=False):
        page.controls.clear()
        screen_main(page, sidebar_open=keep_sidebar_open)
        page.update()

    def go_to_sign_in():
        from sign_in import main as sign_in_main
        page.controls.clear()
        sign_in_main(page)
        page.update()

    # Card builder
    def make_card(title, description, image_path, on_click, expand=1):
        card_content = s.build_card_content(title, description, image_path)
        overlay_button = s.build_card_overlay_button(on_click)

        return ft.Container(
            content=ft.Stack(
                controls=[
                    card_content,
                    overlay_button,
                ],
                expand=True,
            ),
            expand=expand,
            border_radius=s.CARD_RADIUS,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

    # First cards row
    cards_row1 = ft.Row(
        controls=[
            make_card(
                s.DRIVER_TITLE,
                s.DRIVER_DESCRIPTION,
                s.DRIVER_IMAGE,
                on_click=lambda e: go_to(driver_main),
            ),
            make_card(
                s.VEHICLE_TITLE,
                s.VEHICLE_DESCRIPTION,
                s.VEHICLE_IMAGE,
                on_click=lambda e: go_to(vehicle_main),
            ),
        ],
        spacing=s.ROW_SPACING,
        expand=True,
    )

    # Second cards row
    cards_row2 = ft.Row(
        controls=[
            make_card(
                s.REGISTRATION_TITLE,
                s.REGISTRATION_DESCRIPTION,
                s.REGISTRATION_IMAGE,
                on_click=lambda e: go_to(registration_main),
            ),
            make_card(
                s.VIOLATION_TITLE,
                s.VIOLATION_DESCRIPTION,
                s.VIOLATION_IMAGE,
                on_click=lambda e: go_to(violation_main),
            ),
        ],
        spacing=s.ROW_SPACING,
        expand=True,
    )

    # Third cards row
    cards_row3 = ft.Row(
        controls=[
            ft.Container(expand=1),
            make_card(
                s.REPORTS_TITLE,
                s.REPORTS_DESCRIPTION,
                s.REPORTS_IMAGE,
                on_click=lambda e: go_to(reports_main),
                expand=2,
            ),
            ft.Container(expand=1),
        ],
        spacing=s.ROW_SPACING,
        expand=True,
    )

    # Welcome header
    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
    )
    
    header = ft.Container(
        content=ft.Row(
            controls=[
                menu_button,
                ft.Column(
                    controls=[
                        ft.Text(
                            "Welcome!",
                            style=s.HEADER_TITLE_STYLE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "What would you like to do today?",
                            style=s.HEADER_SUBTITLE_STYLE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=s.HEADER_TEXT_SPACING,
                    tight=True,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.alignment.Alignment(0, 0),
        width=float("inf"),
    )

    layout = ft.Column(
        controls=[
            header,
            ft.Container(height=s.HEADER_GAP),
            cards_row1,
            ft.Container(height=s.ROWS_GAP),
            cards_row2,
            ft.Container(height=s.ROWS_GAP),
            cards_row3,
        ],
        expand=True,
        spacing=0,
    )

    # Build sidebar
    def on_menu_item_click(item_name):
        # Handle menu item clicks
        if item_name == "__close__":
            toggle_sidebar(sidebar)
            return
        if item_name == "Sign out":
            go_to_sign_in()
        elif item_name == "Home":
            page.update()
        elif item_name == "Driver":
            go_to(driver_main, keep_sidebar_open=True)
        elif item_name == "Vehicle":
            go_to(vehicle_main, keep_sidebar_open=True)
        elif item_name == "Registration":
            go_to(registration_main, keep_sidebar_open=True)
        elif item_name == "Violation":
            go_to(violation_main, keep_sidebar_open=True)
        elif item_name == "Generate reports":
            go_to(reports_main, keep_sidebar_open=True)
        page.update()

    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Home", is_open=sidebar_open)
    
    menu_button.on_click = lambda e: (toggle_sidebar(sidebar), page.update())

    main_content = ft.Container(
        content=layout,
        padding=s.PAGE_CONTENT_PADDING,
        expand=True,
    )

    # place it on top
    page_stack = ft.Stack(
        controls=[
            main_content,
            sidebar,
        ],
        expand=True,
    )

    page.add(page_stack)