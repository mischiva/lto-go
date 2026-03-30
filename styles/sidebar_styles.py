import flet as ft

# Menu
MENU_ITEMS = [
    "Home",
    "Driver",
    "Vehicle",
    "Registration",
    "Violation",
    "Generate reports",
]

# Dimensions
SIDEBAR_WIDTH = 300
LOGO_SIZE = 80
MENU_ICON_SIZE = 28
SIGN_OUT_WIDTH = 150
SIGN_OUT_HEIGHT = 48

# Spacing and layout
TOP_LOGO_GAP = 10
HEADER_VERTICAL_PADDING = ft.padding.symmetric(vertical=20)
MENU_ITEM_PADDING = ft.padding.symmetric(horizontal=20, vertical=12)
SIGN_OUT_PADDING = ft.padding.symmetric(horizontal=20, vertical=20)

# Colors
SIDEBAR_BG = "#FFFFFF"
TEXT_PRIMARY = "#000000"
TEXT_SECONDARY = "#666666"
DIVIDER = "#E0E0E0"
ACTIVE_BG = "#e7e7e7"
SIGN_OUT_BG = "#0038a8"
SIGN_OUT_HOVER_BG = "#6d8dcc"
SHADOW_COLOR = "#33000000"

# Typography
MENU_ITEM_TEXT_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=16,
    weight=ft.FontWeight.W_500,
    color=TEXT_PRIMARY,
)

BRAND_TITLE_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=24,
    weight=ft.FontWeight.BOLD,
    color=TEXT_PRIMARY,
)

BRAND_SUBTITLE_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=12,
    italic=True,
    color=TEXT_SECONDARY,
)

SIGN_OUT_TEXT_STYLE = ft.TextStyle(
    font_family="Lato",
    weight=ft.FontWeight.W_700,
    size=16,
    color="white",
)

SIGN_OUT_BUTTON_STYLE = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=18),
    bgcolor={
        ft.ControlState.DEFAULT: SIGN_OUT_BG,
        ft.ControlState.HOVERED: SIGN_OUT_HOVER_BG,
    },
)


def is_hovered(data) -> bool:
    return data is True or str(data).lower() == "true"
