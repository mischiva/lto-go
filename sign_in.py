import flet as ft
from styles.fonts import GOOGLE_FONTS
from styles import sign_in_styles as s
from home import main as home_main

def main(page: ft.Page):
    page.title = s.PAGE_TITLE
    page.bgcolor = s.PAGE_BGCOLOR
    page.padding = s.PAGE_PADDING
    page.fonts = GOOGLE_FONTS

    def go_to_home(e):
        page.controls.clear()
        home_main(page, sidebar_open=False)
        page.update()

    layout = ft.Row(
        controls=[
            # Left div
            ft.Container(
                content=ft.Image(
                    src=s.ENTRY_IMAGE_SRC,
                    fit="cover",
                ),
                expand=1,
            ),

            # Right div
            ft.Container(
                content=ft.Column(
                    controls=[
                        # Header
                        ft.Row(
                            controls=[
                                ft.Image(src=s.LOGO_IMAGE_SRC, width=s.LOGO_WIDTH, fit="contain"),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "LTO-Go",
                                            style=s.BRAND_TITLE_STYLE,
                                        ),
                                        ft.Text(
                                            "tracking your every move...",
                                            style=s.BRAND_SUBTITLE_STYLE,
                                            no_wrap=False,
                                            max_lines=2,
                                        ),
                                    ],
                                    spacing=s.HEADER_SUBTITLE_SPACING,
                                    tight=True,
                                    width=s.BRAND_COLUMN_WIDTH,
                                ),
                            ],
                            spacing=s.HEADER_ROW_SPACING,
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        ft.Container(height=s.HEADER_GAP),
                        ft.Column(
                            controls=[
                                # Username
                                ft.Text(
                                    "Username:",
                                    style=s.FIELD_LABEL_STYLE,
                                ),
                                ft.Container(height=s.FIELD_LABEL_GAP),
                                s.build_text_field(hint_text="Enter username"),
                                ft.Container(height=s.FIELDS_GAP),
                                # Password
                                ft.Text(
                                    "Password:",
                                    style=s.FIELD_LABEL_STYLE,
                                ),
                                ft.Container(height=s.FIELD_LABEL_GAP),
                                s.build_text_field(
                                    hint_text="Enter password",
                                    password=True,
                                    can_reveal_password=True,
                                ),
                                ft.Container(height=s.FORM_TO_BUTTON_GAP),
                                # Sign in button
                                ft.Row(
                                    controls=[
                                        ft.Button(
                                            content=ft.Text(
                                                "Sign in",
                                                style=s.BUTTON_TEXT_STYLE,
                                            ),
                                            width=s.BUTTON_WIDTH,
                                            height=s.BUTTON_HEIGHT,
                                            style=s.BUTTON_STYLE,
                                            on_click=go_to_home,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=0,
                            tight=True,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    expand=True,
                ),
                expand=1,
                padding=s.RIGHT_PANEL_PADDING,
            )
        ],
        expand=True
    )

    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)