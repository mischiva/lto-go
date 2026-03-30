import flet as ft

# Sidebar dimensions
SIDEBAR_WIDTH = 250
SIDEBAR_PADDING = ft.padding.all(16)

# Colors
COLOR_SIDEBAR_BG = "#FFFFFF"
COLOR_SIDEBAR_BORDER = "#E0E0E0"
COLOR_MENU_ITEM_HOVER = "#F5F5F5"
COLOR_TEXT_PRIMARY = "#000000"
COLOR_TEXT_SECONDARY = "#666666"
COLOR_PRIMARY = "#0038a8"

# Typography
MENU_ITEM_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=14,
    weight=ft.FontWeight.W500,
    color=COLOR_TEXT_PRIMARY,
)

MENU_SECTION_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=12,
    weight=ft.FontWeight.BOLD,
    color=COLOR_TEXT_SECONDARY,
)

# Spacing
MENU_ITEM_PADDING = ft.padding.symmetric(horizontal=16, vertical=12)
MENU_SECTION_SPACING = 16
MENU_ITEM_SPACING = 8

# Sidebar container
def build_sidebar():
    """Build the sidebar menu"""
    menu_items = ft.Column(
        controls=[
            ft.Text("MENU", style=MENU_SECTION_STYLE),
            build_menu_item("Home", ft.icons.Icons.HOME),
            build_menu_item("Profile", ft.icons.Icons.PERSON),
            build_menu_item("Settings", ft.icons.Icons.SETTINGS),
            build_menu_item("Help", ft.icons.Icons.HELP),
        ],
        spacing=MENU_ITEM_SPACING,
    )

    sidebar = ft.Container(
        content=ft.Column(
            controls=[menu_items],
            scroll=ft.ScrollMode.AUTO,
        ),
        width=SIDEBAR_WIDTH,
        padding=SIDEBAR_PADDING,
        bgcolor=COLOR_SIDEBAR_BG,
        border=ft.border.only(right=ft.BorderSide(1, COLOR_SIDEBAR_BORDER)),
    )

    return sidebar


def build_menu_item(label, icon):
    """Build a single menu item"""
    menu_item = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(name=icon, size=20, color=COLOR_TEXT_PRIMARY),
                ft.Text(label, style=MENU_ITEM_STYLE),
            ],
            spacing=12,
        ),
        padding=MENU_ITEM_PADDING,
        border_radius=8,
        on_hover=lambda e: _on_menu_item_hover(e),
    )

    return menu_item


def _on_menu_item_hover(e):
    """Handle menu item hover"""
    if e.data == "true":
        e.control.bgcolor = COLOR_MENU_ITEM_HOVER
    else:
        e.control.bgcolor = ft.colors.TRANSPARENT
    e.control.update()
