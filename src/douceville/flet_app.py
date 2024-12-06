import flet as ft
from flet.auth.providers import GitHubOAuthProvider
from flet import LoginEvent, Page
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
        if page.auth is None:
            page.login(provider)
            print("Logged in")
        else:
            print("Already logged in")

    def on_login(e: LoginEvent):
        if not e.error:
            pass

    def logout_button_click(e):
        page.logout()
        print("Logged out")

    def on_logout(e):
        pass

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.HOUSE),
        leading_width=40,
        title=ft.Text("Douceville"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE,
        actions=[
            ft.IconButton(ft.Icons.LOGIN, on_click=login_button_click),
            ft.IconButton(ft.Icons.LOGOUT, on_click=logout_button_click),
        ],
    )

    page.add(
        ft.Row(
            [
                # ft.Container(
                #     content=ft.Text("Non clickable"),
                #     margin=10,
                #     padding=10,
                #     alignment=ft.alignment.center,
                #     bgcolor=ft.Colors.AMBER,
                #     width=150,
                #     height=150,
                #     border_radius=10,
                # ),
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

    page.on_login = on_login
    page.on_logout = on_logout


# hypercorn douceville.flet_app:app --bind 0.0.0.0:3566
app = ft.app(main, export_asgi_app=True)
