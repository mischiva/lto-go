import flet as ft

COLOR_PRIMARY = "#0038a8"
COLOR_PRIMARY_HOVER = "#6d8dcc"
COLOR_BORDER = "#e3e3e3"
COLOR_FIELD_FILL = "#f9f9f9"
COLOR_TEXT_PRIMARY = "#111111"
COLOR_TEXT_HINT = "#5f6368"

TITLE_STYLE = ft.TextStyle(
    font_family="DM Sans",
    size=40,
    weight=ft.FontWeight.BOLD,
    color=COLOR_PRIMARY,
)

SECTION_TITLE_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=18,
    weight=ft.FontWeight.W_700,
    color="#111111",
)

LABEL_STYLE = ft.TextStyle(
    font_family="Lato",
    size=14,
    weight=ft.FontWeight.W_700,
    color="#222222",
)

TABLE_HEADER_STYLE = ft.TextStyle(
    font_family="Lato",
    size=13,
    weight=ft.FontWeight.W_700,
    color="#111111",
)

TABLE_DATA_STYLE = ft.TextStyle(
    font_family="Lato",
    size=13,
    weight=ft.FontWeight.W_500,
    color=COLOR_TEXT_PRIMARY,
)

BLUE_BUTTON_STYLE = ft.ButtonStyle(
    bgcolor={
        ft.ControlState.DEFAULT: COLOR_PRIMARY,
        ft.ControlState.HOVERED: COLOR_PRIMARY_HOVER,
    },
    shape=ft.RoundedRectangleBorder(radius=12),
)
