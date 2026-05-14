# style configuration specifically for the sign-in hero screen
# we keep all the login-specific colors and field sizes here
import flet as ft

# basic meta settings for the login page
PAGE_TITLE = "LTO-Go"
PAGE_BGCOLOR = "white"
PAGE_PADDING = 0

# paths to the branding images used on the login screen
ENTRY_IMAGE_SRC = "media/entry.png"
LOGO_IMAGE_SRC = "media/logo.png"
LOGO_WIDTH = 250

# specific padding for the right half of the split screen where the form lives
RIGHT_PANEL_PADDING = ft.padding.only(top=90, left=50, right=50)
HEADER_ROW_SPACING = 16
HEADER_SUBTITLE_SPACING = -20
HEADER_GAP = 24
FIELD_LABEL_GAP = 6
FIELDS_GAP = 16
FORM_TO_BUTTON_GAP = 28

# size constants to make sure the login form doesnt look too wide or too narrow
BRAND_COLUMN_WIDTH = 370
TEXT_FIELD_HEIGHT = 52
BUTTON_WIDTH = 240
BUTTON_HEIGHT = 62
TEXTFIELD_BORDER_RADIUS = 34
BUTTON_RADIUS = 18

# COLOR PALETTE
COLOR_BLACK = "#000000"
COLOR_TEXT_PRIMARY = "#111111"
COLOR_TEXT_HINT = "#666666"
COLOR_TEXT_INVERSE = "#ffffff"
COLOR_FIELD_FILL = "#f9f9f9"
COLOR_FIELD_BORDER = "#e7e7e7"
COLOR_BUTTON_DEFAULT = "#0038a8"
COLOR_BUTTON_HOVER = "#6d8dcc"

# BRAND TITLE
BRAND_TITLE_STYLE = ft.TextStyle(
    font_family="DM Sans",
    weight=ft.FontWeight.W_900,
    size=92,
    color=COLOR_BLACK,
)

# BRAND SUBTITLE
BRAND_SUBTITLE_STYLE = ft.TextStyle(
    font_family="Roboto",
    italic=True,
    size=35,
    color=COLOR_BLACK,
)

# FIELD LABEL
FIELD_LABEL_STYLE = ft.TextStyle(
    font_family="Lato",
    weight=ft.FontWeight.W_700,
    size=18,
    color=COLOR_TEXT_PRIMARY,
)

# FIELD TEXT
FIELD_TEXT_STYLE = ft.TextStyle(
    font_family="Lato",
    weight=ft.FontWeight.W_400,
    size=16,
    color=COLOR_TEXT_PRIMARY,
)

# FIELD HINT
FIELD_HINT_STYLE = ft.TextStyle(
    font_family="Lato",
    weight=ft.FontWeight.W_400,
    size=16,
    color=COLOR_TEXT_HINT,
)

# BUTTON TEXT
BUTTON_TEXT_STYLE = ft.TextStyle(
    font_family="Lato",
    weight=ft.FontWeight.W_700,
    size=16,
    color=COLOR_TEXT_INVERSE,
)

# BUTTON STYLE
BUTTON_STYLE = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=BUTTON_RADIUS),
    bgcolor={
        ft.ControlState.DEFAULT: COLOR_BUTTON_DEFAULT,
        ft.ControlState.HOVERED: COLOR_BUTTON_HOVER,
    },
)


def build_text_field(hint_text: str, password: bool = False, can_reveal_password: bool = False) -> ft.TextField:
    # para tong approach ko ay reusable text field na may specific theme para sa sign in
    return ft.TextField(
        hint_text=hint_text,
        password=password,
        can_reveal_password=can_reveal_password,
        text_style=FIELD_TEXT_STYLE,
        hint_style=FIELD_HINT_STYLE,
        filled=True,
        fill_color=COLOR_FIELD_FILL,
        border_color=COLOR_FIELD_BORDER,
        focused_border_color=COLOR_FIELD_BORDER,
        border_radius=TEXTFIELD_BORDER_RADIUS,
        cursor_color=COLOR_TEXT_PRIMARY,
        height=TEXT_FIELD_HEIGHT,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=0),
        expand=True,
    )
