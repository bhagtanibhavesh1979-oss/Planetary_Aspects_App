import flet as ft
from ui.tables import PlanetaryPositionsTable, AspectsTable, PlanetSummaryTable
from ui.settings import SettingsSidebar

class AppLayout(ft.Column):
    def __init__(self, on_settings_change, default_orb, default_rules, default_specific_rules, default_range_rules):
        super().__init__(expand=True)
        
        self.positions_table = PlanetaryPositionsTable()
        self.summary_table = PlanetSummaryTable()
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
                        ft.Text("Positions", size=20, weight=ft.FontWeight.BOLD),
                        self.positions_table
                    ], scroll=ft.ScrollMode.AUTO),
                    width=200,  # Compact width
                    padding=5,
                    border=ft.border.all(1, "grey300"),
                    border_radius=5,
                    expand=False
                ),
                # Summary Column
                ft.Container(
                    content=ft.Column([
                        ft.Text("Summary", size=20, weight=ft.FontWeight.BOLD),
                        self.summary_table
                    ], scroll=ft.ScrollMode.AUTO),
                    width=240,  # Compact width
                    padding=5,
                    border=ft.border.all(1, "grey300"),
                    border_radius=5,
                    expand=False
                ),
                # Center Column: Aspects
                ft.Container(
                    content=ft.Column([
                        ft.Text("Aspects", size=20, weight=ft.FontWeight.BOLD),
                        self.aspects_table
                    ], scroll=ft.ScrollMode.AUTO),
                    width=480, # Initial width, will be updated
                    padding=5,
                    border=ft.border.all(1, "grey300"),
                    border_radius=5,
                    expand=False,
                    ref=ft.Ref() # Add ref if needed, or just assign to self
                ),
                # Right Column: Settings
                ft.Container(
                    content=self.settings_sidebar,
                    width=240, # Reduced width
                    padding=5,
                    border=ft.border.all(1, "grey300"),
                    border_radius=5,
                    bgcolor="grey50"
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO # Enable scrolling if window is too small
        )
        
        # Store reference to aspects container for resizing
        self.aspects_container = self.content_row.controls[2] 
        
        self.controls = [
            self.header,
            self.content_row
        ]

    def resize(self, page_width):
        # Fixed widths: Positions(200) + Summary(240) + Settings(240) + Padding/Margins(~40)
        fixed_width = 200 + 240 + 240 + 60 
        min_aspects_width = 480
        
        # Calculate new width
        new_width = max(min_aspects_width, page_width - fixed_width)
        
        self.aspects_container.width = new_width
        self.aspects_container.update()
