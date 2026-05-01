# pulling in flet for building the sidebar ui
import flet as ft
# getting our sidebar styles
from styles import sidebar_styles as s


def build_sidebar(page, on_menu_click, current_screen="Home", is_open=False):
    # building the list of navigation items dynamically from our style sheet

    menu_controls = []
    for item_name in s.MENU_ITEMS:
        is_active = item_name == current_screen
        # Build individual menu item container
        menu_item = ft.Container(
            content=ft.Text(
                item_name,
                style=s.MENU_ITEM_TEXT_STYLE,
            ),
            width=float("inf"),
            alignment=ft.Alignment.CENTER_LEFT,
            padding=s.MENU_ITEM_PADDING,
            # highlighting the item if it matches the screen we are currently on
            bgcolor=s.ACTIVE_BG if is_active else None,
            data={"active": is_active},
            on_hover=_on_menu_item_hover,
            on_click=lambda e, name=item_name: on_menu_click(name),
        )
        menu_controls.append(menu_item)

    sidebar_content = ft.Column(
        # arranging the sidebar elements vertically
        controls=[
            ft.Container(
                # top section with the logo and brand tagline
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.Icons.MENU,
                                    icon_size=s.MENU_ICON_SIZE,
                                    icon_color=ft.Colors.BLACK,
                                    on_click=lambda e: on_menu_click("__close__"),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        ft.Container(height=s.TOP_LOGO_GAP),
                        ft.Image(
                            src="media/logo.png",
                            width=s.LOGO_SIZE,
                            height=s.LOGO_SIZE,
                            fit=ft.BoxFit.CONTAIN,
                        ),
                        ft.Text(
                            "LTO-Go",
                            style=s.BRAND_TITLE_STYLE,
                        ),
                        ft.Text(
                            "tracking your every move...",
                            style=s.BRAND_SUBTITLE_STYLE,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                ),
                padding=s.HEADER_VERTICAL_PADDING,
            ),

            # Decorative horizontal line separating header from navigation
            ft.Container(height=1, bgcolor=s.DIVIDER),

            # List of navigation links generated earlier
            ft.Column(
                controls=menu_controls,
                spacing=0,
                width=float("inf"),
            ),

            # Flexible container that absorbs extra vertical space
            ft.Container(expand=True),

            # Sign out trigger at the bottom of the sidebar
            ft.Container(
                content=ft.Button(
                    content=ft.Text("Sign out", style=s.SIGN_OUT_TEXT_STYLE),
                    width=s.SIGN_OUT_WIDTH,
                    height=s.SIGN_OUT_HEIGHT,
                    style=s.SIGN_OUT_BUTTON_STYLE,
                    on_click=lambda e: on_menu_click("Sign out"),
                ),
                alignment=ft.Alignment.CENTER,
                padding=s.SIGN_OUT_PADDING,
            ),
        ],
        spacing=0,
        expand=True,
    )

    # The outer sidebar shell using Offset for the slide animation
    sidebar = ft.Container(
        content=sidebar_content,
        width=s.SIDEBAR_WIDTH,
        bgcolor=s.SIDEBAR_BG,
        # Initial position: x=0 (visible) or x=-1 (hidden off-screen to the left)
        offset=ft.Offset(0, 0) if is_open else ft.Offset(-1, 0),
        animate_offset=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
        shadow=ft.BoxShadow(blur_radius=18, color=s.SHADOW_COLOR, offset=ft.Offset(2, 0)),
    )

    return sidebar


# Logic function to switch the visibility state of the sidebar container
def toggle_sidebar(sidebar):
    if sidebar.offset.x == -1:
        sidebar.offset = ft.Offset(0, 0) # Slide in
    else:
        sidebar.offset = ft.Offset(-1, 0) # Slide out
    sidebar.update()


# Internal helper to manage the visual background color during hover interactions
def _on_menu_item_hover(e):
    # Parse the boolean hover state from Flet event data
    is_hovered = s.is_hovered(e.data)
    is_active = bool(e.control.data and e.control.data.get("active"))
    if is_active:
        e.control.bgcolor = s.ACTIVE_BG
    else:
        e.control.bgcolor = s.ACTIVE_BG if is_hovered else None
    e.control.update()
