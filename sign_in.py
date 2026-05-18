import flet as ft
import psycopg2

from home import main as home_main
from styles.fonts import GOOGLE_FONTS
from styles import sign_in_styles as s

# test account natin ito
# username: admin.lto@gov.ph
# password: endthesem


def connectDatabase():
    return psycopg2.connect(host="localhost", port="5432", dbname="lto-go", user="postgres", password="useruser")


def main(page: ft.Page):
    page.title = s.PAGE_TITLE
    page.bgcolor = s.PAGE_BGCOLOR
    page.padding = s.PAGE_PADDING
    page.fonts = GOOGLE_FONTS

    username_field = s.build_text_field(hint_text="Enter username")
    password_field = s.build_text_field(
        hint_text="Enter password",
        password=True,
        can_reveal_password=True,
    )
    error_text = ft.Text("", color=ft.Colors.RED, size=14)

    def go_to_home(e):
        try:
            username = username_field.value.strip()
            password = password_field.value.strip()

            with connectDatabase() as server:
                with server.cursor() as cur:
                    cur.execute(
                        "SELECT 1 FROM app_users WHERE username = %s AND password = %s",
                        (username, password),
                    )
                    if cur.fetchone() is None:
                        raise ValueError("invalid credentials")

            error_text.value = ""
            page.controls.clear()
            home_main(page, sidebar_open=False)
            page.update()
        except Exception:
            error_text.value = "Invalid! Try again."
            page.update()

    layout = ft.Row(
        controls=[
            ft.Container(
                content=ft.Image(
                    src=s.ENTRY_IMAGE_SRC,
                    fit="cover",
                ),
                expand=1,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Image(src=s.LOGO_IMAGE_SRC, width=s.LOGO_WIDTH, fit="contain"),
                                ft.Column(
                                    controls=[
                                        ft.Text("LTO-Go", style=s.BRAND_TITLE_STYLE),
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
                                ft.Text("Username:", style=s.FIELD_LABEL_STYLE),
                                ft.Container(height=s.FIELD_LABEL_GAP),
                                username_field,
                                ft.Container(height=s.FIELDS_GAP),
                                ft.Text("Password:", style=s.FIELD_LABEL_STYLE),
                                ft.Container(height=s.FIELD_LABEL_GAP),
                                password_field,
                                ft.Container(height=s.FORM_TO_BUTTON_GAP),
                                ft.Row(
                                    controls=[
                                        ft.Button(
                                            content=ft.Text("Sign in", style=s.BUTTON_TEXT_STYLE),
                                            width=s.BUTTON_WIDTH,
                                            height=s.BUTTON_HEIGHT,
                                            style=s.BUTTON_STYLE,
                                            on_click=go_to_home,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                error_text,
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
            ),
        ],
        expand=True,
    )

    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)
