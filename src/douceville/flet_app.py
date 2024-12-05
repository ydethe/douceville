import flet as ft
from flet.auth.providers import GitHubOAuthProvider
from flet import ElevatedButton, LoginEvent, Page
import flet.map as fmap

from .config import config


def main(page: Page):

    page.title = "Douceville"
    page.adaptive = True

    provider = GitHubOAuthProvider(
        client_id=config.GITHUB_CLIENT_ID,
        client_secret=config.GITHUB_CLIENT_SECRET,
        redirect_url="http://localhost:3566/oauth_callback",
    )

    # marker_layer_ref = ft.Ref[fmap.MarkerLayer]()

    def login_button_click(e):
        page.login(provider)

    def on_login(e: LoginEvent):
        if not e.error:
            toggle_login_buttons()

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        toggle_login_buttons()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logout_button.visible = page.auth is not None
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.HOUSE),
        leading_width=40,
        title=ft.Text("Douceville"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE,
        actions=[
            ft.IconButton(ft.Icons.LOGOUT, on_click=logout_button_click),
        ],
    )

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Text("Non clickable"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.AMBER,
                    width=150,
                    height=150,
                    border_radius=10,
                ),
                fmap.Map(
                    expand=True,
                    initial_center=fmap.MapLatitudeLongitude(45, 2),
                    initial_zoom=5,
                    interaction_configuration=fmap.MapInteractionConfiguration(
                        flags=fmap.MapInteractiveFlag.ALL
                    ),
                    # on_init=lambda e: print("Initialized Map"),
                    # on_tap=lambda e: print("on_tap", e),
                    # on_secondary_tap=lambda e: print("on_secondary_tap",e),
                    # on_long_press=lambda e: print("on_long_press",e),
                    # on_event=lambda e: print(e),
                    layers=[
                        fmap.TileLayer(
                            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                            on_image_error=lambda e: print("TileLayer Error"),
                        ),
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    login_button = ElevatedButton("Login with GitHub", on_click=login_button_click)
    logout_button = ElevatedButton("Logout", on_click=logout_button_click)
    toggle_login_buttons()
    page.on_login = on_login
    page.on_logout = on_logout
    page.add(login_button, logout_button)


# hypercorn douceville.flet_app:app --bind 0.0.0.0:3566
app = ft.app(main, export_asgi_app=True)
