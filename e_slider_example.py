import flet as ft
from flet_extra import ESlider


def main(page: ft.Page):
    page.theme_mode = 'dark'
    page.theme = ft.theme.Theme(color_scheme_seed='#ddaa00')
    page.spacing = 60


    page.add(
        ft.Column(
            controls=[
                ESlider(on_change=lambda x: print(f'{x:g}'), bgcolor='#999900', color='#88ffffff', margin=5, thickness=30),
                ESlider(value=150, color='orange', length=400, max=200, min=100, divisions=5, margin=4, thickness=50, border_radius=15, on_change=lambda x: print(f'{x:g}')),
                ESlider(color='purple', margin=3, on_change=lambda x: print(f'{x:g}')),
            ],
            spacing=50,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        ft.Row(
            controls=[
                ESlider(value=100, orientation='vertical', color='orange', margin=-4, on_change=lambda x: print(f'{x:g}')),
                ESlider(orientation='vertical', margin=4, on_change=lambda x: print(f'{x:g}')),
                ESlider(orientation='vertical', thickness=50, bgcolor='#226644', border_radius=10, margin=-5, color='amber', on_change=lambda x: print(f'{x:g}')),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
    )


ft.app(target=main)