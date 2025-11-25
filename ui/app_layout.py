import flet as ft
from ui.tables import PlanetaryPositionsTable, AspectsTable
from ui.settings import SettingsSidebar

class AppLayout(ft.Column):
    def __init__(self, on_settings_change, default_orb, default_rules, default_specific_rules, default_range_rules):
        super().__init__(expand=True)
        
        self.positions_table = PlanetaryPositionsTable()
        self.aspects_table = AspectsTable()
        self.settings_sidebar = SettingsSidebar(on_settings_change, default_orb, default_rules, default_specific_rules, default_range_rules)
        
        # Header
        self.header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Planetary Aspects Analyzer", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Text("Sidereal (Lahiri)", italic=True)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10,
            bgcolor="bluegrey100",
            border_radius=5
        )
        
        # Main Content Area
        self.content_row = ft.Row(
            controls=[
                # Left Column: Positions
                ft.Container(
                    content=ft.Column([
                        ft.Text("Planetary Positions", size=20, weight=ft.FontWeight.BOLD),
                        self.positions_table
                    ], scroll=ft.ScrollMode.AUTO),
                    width=300,
                    padding=10,
                    border=ft.border.all(1, "grey300"),
                    border_radius=5,
                    expand=False
                ),
                # Center Column: Aspects
                ft.Container(
                    content=ft.Column([
                        ft.Text("Aspects & Trends", size=20, weight=ft.FontWeight.BOLD),
                        self.aspects_table
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=10,
                    border=ft.border.all(1, "grey300"),
                    border_radius=5,
                    expand=True
                ),
                # Right Column: Settings
                ft.Container(
                    content=self.settings_sidebar,
                    width=350,
                    padding=10,
                    border=ft.border.all(1, "grey300"),
                    border_radius=5,
                    bgcolor="grey50"
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        
        self.controls = [
            self.header,
            self.content_row
        ]
