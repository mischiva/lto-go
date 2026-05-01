# HOMEPAGE STYLES:
# This contains all styles for the home page

import flet as ft

PAGE_BGCOLOR = "white"
PAGE_PADDING = 0
PAGE_CONTENT_PADDING = ft.padding.symmetric(horizontal=40, vertical=30)

ROW_SPACING = 16
HEADER_GAP = 20
ROWS_GAP = 8
HEADER_TEXT_SPACING = 2

CARD_HEIGHT = 180
CARD_RADIUS = 14

CARD_TEXT_SPACING = 4
CARD_TEXT_PADDING = ft.padding.all(16)

# COLOR PALETTE
COLOR_BLACK = "#000000"
COLOR_PRIMARY = "#0038a8"
COLOR_TRANSPARENT = "#00000000"
COLOR_CARD_HOVER_OVERLAY = "#2D000000"

# TITLE
HEADER_TITLE_STYLE = ft.TextStyle(
    font_family="DM Sans",
    size=48,
    weight=ft.FontWeight.BOLD,
    color=COLOR_PRIMARY,
)

# GREETING TEXT
HEADER_SUBTITLE_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=16,
    weight=ft.FontWeight.BOLD,
    italic=True,
    color=COLOR_BLACK,
)

# CARD NAMES
CARD_TITLE_STYLE = ft.TextStyle(
    font_family="Roboto",
    size=20,
    weight=ft.FontWeight.BOLD,
    color=COLOR_BLACK,
)

# CARD DESCRIPTION
CARD_DESCRIPTION_STYLE = ft.TextStyle(
    font_family="Lato",
    size=12,
    color=COLOR_BLACK,
)

# TEXT
DRIVER_TITLE = "Driver"
DRIVER_DESCRIPTION = "Add, update, delete, and search driver records and license information."
DRIVER_IMAGE = "media/driver.png"

VEHICLE_TITLE = "Vehicle"
VEHICLE_DESCRIPTION = "Manage vehicle records, ownership, and associated driver information."
VEHICLE_IMAGE = "media/vehicle.png"

REGISTRATION_TITLE = "Registration"
REGISTRATION_DESCRIPTION = "Record and renew vehicle registrations. View registration history per vehicle."
REGISTRATION_IMAGE = "media/registration.png"

VIOLATION_TITLE = "Violation"
VIOLATION_DESCRIPTION = "Log and manage traffic violations, fines, and apprehension details."
VIOLATION_IMAGE = "media/violation.png"

REPORTS_TITLE = "Generate reports"
REPORTS_DESCRIPTION = "Get summaries and insights on drivers, vehicles, registrations, and violations."
REPORTS_IMAGE = "media/report.png"


# para tong ang approach ko ay like ito ay react component kunyare
# tapos may function dito sa styles keme saka lang to cacall / import dun sa home mismo
# dibaaa wow
def build_card_content(title: str, description: str, image_path: str) -> ft.Container:
    return ft.Container(
        content=ft.Stack(
            controls=[
                ft.Image(
                    src=image_path,
                    fit="cover",
                    width=float("inf"),
                    height=float("inf"),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(title, style=CARD_TITLE_STYLE),
                            ft.Text(
                                description,
                                style=CARD_DESCRIPTION_STYLE,
                                no_wrap=False,
                                max_lines=3,
                            ),
                        ],
                        spacing=CARD_TEXT_SPACING,
                        tight=True,
                    ),
                    padding=CARD_TEXT_PADDING,
                    alignment=ft.alignment.Alignment(-1, -1),
                    expand=True,
                ),
            ],
            expand=True,
        ),
        border_radius=CARD_RADIUS,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        expand=True,
        height=CARD_HEIGHT,
    )


def build_card_overlay_button(on_click) -> ft.Container:
    # overlay to para dun sa medjo grayish look 
    overlay_button = ft.Container(
        expand=True,
        height=CARD_HEIGHT,
        bgcolor=COLOR_TRANSPARENT,
        border_radius=CARD_RADIUS,
        on_click=on_click,
        ink=False,
    )

    def on_overlay_hover(e: ft.HoverEvent):
        # when the user hovers over a card we add a slight dark tint so they know it is clickable
        is_hovered = e.data is True or str(e.data).lower() == "true"
        overlay_button.bgcolor = COLOR_CARD_HOVER_OVERLAY if is_hovered else COLOR_TRANSPARENT
        overlay_button.update()

    overlay_button.on_hover = on_overlay_hover
    return overlay_button
