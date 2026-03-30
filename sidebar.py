import flet as ft
from styles import sidebar_styles as s


def build_sidebar(page, on_menu_click, current_screen="Home", is_open=False):
    """Build sidebar with animation"""

    # Build menu item controls
    menu_controls = []
    for item_name in s.MENU_ITEMS:
        is_active = item_name == current_screen
        menu_item = ft.Container(
            content=ft.Text(
                item_name,
                style=s.MENU_ITEM_TEXT_STYLE,
            ),
            width=float("inf"),
            alignment=ft.Alignment.CENTER_LEFT,
            padding=s.MENU_ITEM_PADDING,
            bgcolor=s.ACTIVE_BG if is_active else None,
            data={"active": is_active},
            on_hover=_on_menu_item_hover,
            on_click=lambda e, name=item_name: on_menu_click(name),
        )
        menu_controls.append(menu_item)

    # Sidebar content
    sidebar_content = ft.Column(
        controls=[
            # Logo and header section
            ft.Container(
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

            # Divider
            ft.Container(height=1, bgcolor=s.DIVIDER),

            # Menu items
            ft.Column(
                controls=menu_controls,
                spacing=0,
                width=float("inf"),
            ),

            # Spacer to push sign out to bottom
            ft.Container(expand=True),

            # Sign out button
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

    # Sidebar container
    sidebar = ft.Container(
        content=sidebar_content,
        width=s.SIDEBAR_WIDTH,
        bgcolor=s.SIDEBAR_BG,
        offset=ft.Offset(0, 0) if is_open else ft.Offset(-1, 0),
        animate_offset=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
        shadow=ft.BoxShadow(blur_radius=18, color=s.SHADOW_COLOR, offset=ft.Offset(2, 0)),
    )

    return sidebar


def toggle_sidebar(sidebar):
    """Toggle sidebar visibility with animation"""
    if sidebar.offset.x == -1:
        sidebar.offset = ft.Offset(0, 0)
    else:
        sidebar.offset = ft.Offset(-1, 0)
    sidebar.update()


def _on_menu_item_hover(e):
    is_hovered = s.is_hovered(e.data)
    is_active = bool(e.control.data and e.control.data.get("active"))
    if is_active:
        e.control.bgcolor = s.ACTIVE_BG
    else:
        e.control.bgcolor = s.ACTIVE_BG if is_hovered else None
    e.control.update()
