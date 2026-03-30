import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Container(
            content=ft.Text("Violation", size=40, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.Alignment(0, 0),
            expand=True,
        )
    )
