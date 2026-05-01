# REGISTRATION STYLES:
# This contains all styles for the registration module

import flet as ft

# COLOR PALETTE
COLOR_PRIMARY = "#0038a8"
COLOR_PRIMARY_HOVER = "#6d8dcc"
COLOR_BORDER = "#e3e3e3"
COLOR_FIELD_FILL = "#f9f9f9"
COLOR_TEXT_PRIMARY = "#111111"
COLOR_TEXT_HINT = "#5f6368"

# the giant header at the top of the registration page using that dm sans font for a modern look
TITLE_STYLE = ft.TextStyle(
    font_family="DM Sans",
    size=40,
    weight=ft.FontWeight.BOLD,
    color=COLOR_PRIMARY,
)

# for subheadings
SECTION_TITLE_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=18,
    weight=ft.FontWeight.W_700,
    color="#111111",
)

# for little labels
LABEL_STYLE = ft.TextStyle(
    font_family="Lato",
    size=14,
    weight=ft.FontWeight.W_700,
    color="#222222",
)

# for column headers in the table
TABLE_HEADER_STYLE = ft.TextStyle(
    font_family="Lato",
    size=13,
    weight=ft.FontWeight.W_700,
    color="#111111",
)

# for rows in the table
TABLE_DATA_STYLE = ft.TextStyle(
    font_family="Lato",
    size=13,
    weight=ft.FontWeight.W_500,
    color=COLOR_TEXT_PRIMARY,
)

# for the button
# BLUE BUTTON STYLE
BLUE_BUTTON_STYLE = ft.ButtonStyle(
    bgcolor={
        ft.ControlState.DEFAULT: COLOR_PRIMARY,
        ft.ControlState.HOVERED: COLOR_PRIMARY_HOVER,
    },
    shape=ft.RoundedRectangleBorder(radius=12),
)
