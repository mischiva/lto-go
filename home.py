# pulling in flet so we can actually build this cross platform ui
import flet as ft
# getting our global fonts so all our text looks clean and consistent
from styles.fonts import GOOGLE_FONTS
# using s as an alias for our home styles so we don't have to type out the whole name every time
from styles import home_styles as s
from sidebar import build_sidebar, toggle_sidebar
from driver import main as driver_main
from vehicle import main as vehicle_main
from registration import main as registration_main
from violation import main as violation_main
from reports import main as reports_main


# this is the main hub for the dashboard where users decide where to go next
def main(page: ft.Page, sidebar_open=False):
    # setting up the background and padding based on our style sheet
    page.bgcolor = s.PAGE_BGCOLOR
    page.padding = s.PAGE_PADDING
    # registering our fonts so flet knows how to render the custom typography
    page.fonts = GOOGLE_FONTS

    def go_to(screen_main, keep_sidebar_open=False):
        # we wipe the page clean before mounting the new screen so nothing overlaps
        page.controls.clear()
        screen_main(page, sidebar_open=keep_sidebar_open)
        page.update()

    def go_to_sign_in():
        # specific exit logic to take the user back to the login screen
        from sign_in import main as sign_in_main
        page.controls.clear()
        sign_in_main(page)
        page.update()

    def make_card(title, description, image_path, on_click, expand=1):
        # this helper builds those big navigation cards by stacking the image and text together
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

    # first row of navigation cards for drivers and vehicles
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

    # Layout organization: Second row contains Registration and Violation modules
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

    # third row specifically for generating reports which we center by using spacers
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

    # setting up the menu icon at the top left
    menu_button = ft.IconButton(
        icon=ft.icons.Icons.MENU,
        icon_size=28,
        icon_color=ft.Colors.BLACK,
    )
    
    header = ft.Container(
        content=ft.Row(
            controls=[
                menu_button, # Triggers the sidebar
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

    def on_menu_item_click(item_name):
        # this handles the logic whenever someone clicks an item in the sidebar
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

    # building the sidebar and passing in the current screen name so it knows what to highlight
    sidebar = build_sidebar(page, on_menu_item_click, current_screen="Home", is_open=sidebar_open)
    
    # linking the header menu button to the sidebar toggle function
    menu_button.on_click = lambda e: (toggle_sidebar(sidebar), page.update())

    main_content = ft.Container(
        content=layout,
        padding=s.PAGE_CONTENT_PADDING,
        expand=True,
    )

    page_stack = ft.Stack(
        controls=[
            main_content,
            sidebar,
        ],
        expand=True,
    )

    page.add(page_stack)