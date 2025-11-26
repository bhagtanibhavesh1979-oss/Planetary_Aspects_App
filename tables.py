import flet as ft

class PlanetaryPositionsTable(ft.Column):
    def __init__(self):
        super().__init__(scroll=ft.ScrollMode.AUTO)
        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Planet", weight=ft.FontWeight.BOLD, expand=1),
                    ft.Text("Deg", weight=ft.FontWeight.BOLD, expand=1),
                ],
            ),
            padding=5,
            bgcolor="grey200",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "grey400")),
        )
        self.rows_col = ft.Column(spacing=0)
        self.controls = [self.header, self.rows_col]

    def update_data(self, positions: dict):
        self.rows_col.controls = []
        for i, (planet, deg) in enumerate(positions.items()):
            bg_color = "white" if i % 2 == 0 else "grey50"
            self.rows_col.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(planet, expand=1),
                            ft.Text(f"{deg:.2f}°", expand=1),
                        ],
                    ),
                    padding=5,
                    bgcolor=bg_color,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "grey200"))
                )
            )
        self.update()

class PlanetSummaryTable(ft.Column):
    def __init__(self):
        super().__init__(scroll=ft.ScrollMode.AUTO)
        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Planet", weight=ft.FontWeight.BOLD, expand=2),
                    ft.Text("Tot", weight=ft.FontWeight.BOLD, expand=1, text_align=ft.TextAlign.CENTER),
                    ft.Text("Pos", weight=ft.FontWeight.BOLD, expand=1, text_align=ft.TextAlign.CENTER),
                    ft.Text("Neg", weight=ft.FontWeight.BOLD, expand=1, text_align=ft.TextAlign.CENTER),
                ],
            ),
            padding=5,
            bgcolor="grey200",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "grey400")),
        )
        self.rows_col = ft.Column(spacing=0)
        self.controls = [self.header, self.rows_col]

    def update_data(self, summary: dict):
        self.rows_col.controls = []
        
        grand_total = 0
        grand_pos = 0
        grand_neg = 0
        
        for i, planet in enumerate(sorted(summary.keys())):
            stats = summary[planet]
            grand_total += stats["total"]
            grand_pos += stats["positive"]
            grand_neg += stats["negative"]
            
            bg_color = "white" if i % 2 == 0 else "grey50"
            self.rows_col.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(planet, weight=ft.FontWeight.BOLD, expand=2),
                            ft.Text(str(stats["total"]), expand=1, text_align=ft.TextAlign.CENTER),
                            ft.Text(str(stats["positive"]), color="green", weight=ft.FontWeight.BOLD, expand=1, text_align=ft.TextAlign.CENTER),
                            ft.Text(str(stats["negative"]), color="red", weight=ft.FontWeight.BOLD, expand=1, text_align=ft.TextAlign.CENTER),
                        ],
                    ),
                    padding=5,
                    bgcolor=bg_color,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "grey200"))
                )
            )
            
        # Add Grand Total Row
        self.rows_col.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("TOTAL", weight=ft.FontWeight.BOLD, expand=2),
                        ft.Text(str(grand_total), weight=ft.FontWeight.BOLD, expand=1, text_align=ft.TextAlign.CENTER),
                        ft.Text(str(grand_pos), color="green", weight=ft.FontWeight.BOLD, expand=1, text_align=ft.TextAlign.CENTER),
                        ft.Text(str(grand_neg), color="red", weight=ft.FontWeight.BOLD, expand=1, text_align=ft.TextAlign.CENTER),
                    ],
                ),
                padding=5,
                bgcolor="grey300", # Distinct background
                border=ft.border.only(top=ft.border.BorderSide(2, "grey500")) # Top border to separate
            )
        )
        self.update()

class AspectsTable(ft.Column):
    def __init__(self):
        super().__init__(scroll=ft.ScrollMode.AUTO)
        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("P1", weight=ft.FontWeight.BOLD, expand=1),
                    ft.Text("P2", weight=ft.FontWeight.BOLD, expand=1),
                    ft.Text("Angle", weight=ft.FontWeight.BOLD, expand=1),
                    ft.Text("Aspect", weight=ft.FontWeight.BOLD, expand=2),
                    ft.Text("Trend", weight=ft.FontWeight.BOLD, expand=1),
                ],
            ),
            padding=5, # Reduced padding
            bgcolor="grey200",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "grey400")),
        )
        self.rows_col = ft.Column(spacing=0)
        self.controls = [self.header, self.rows_col]

    def update_data(self, aspects: list):
        self.rows_col.controls = []
        for i, aspect in enumerate(aspects):
            trend = aspect["trend"]
            color = "black"
            if trend == "Positive":
                color = "green"
            elif trend == "Negative":
                color = "red"
            elif trend == "Neutral":
                color = "blue"
            
            bg_color = "white" if i % 2 == 0 else "grey50"
            
            self.rows_col.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(aspect["planet1"], expand=1),
                            ft.Text(aspect["planet2"], expand=1),
                            ft.Text(f"{aspect['angle_deg']:.2f}°", expand=1),
                            ft.Text(aspect["aspect_name"], expand=2),
                            ft.Text(trend, color=color, weight=ft.FontWeight.BOLD, expand=1),
                        ],
                    ),
                    padding=5, # Reduced padding
                    bgcolor=bg_color,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "grey200"))
                )
            )
        self.update()
