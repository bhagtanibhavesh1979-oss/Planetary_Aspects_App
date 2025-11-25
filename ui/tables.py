import flet as ft

class PlanetaryPositionsTable(ft.DataTable):
    def __init__(self):
        super().__init__(
            columns=[
                ft.DataColumn(ft.Text("Planet")),
                ft.DataColumn(ft.Text("Degree (Sidereal)")),
            ],
            rows=[],
            border=ft.border.all(1, "grey400"),
            vertical_lines=ft.border.all(1, "grey400"),
            horizontal_lines=ft.border.all(1, "grey400"),
        )

    def update_data(self, positions: dict):
        self.rows = []
        for planet, deg in positions.items():
            self.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(planet)),
                        ft.DataCell(ft.Text(f"{deg:.2f}°")),
                    ]
                )
            )
        self.update()

class AspectsTable(ft.DataTable):
    def __init__(self):
        super().__init__(
            columns=[
                ft.DataColumn(ft.Text("Planet 1")),
                ft.DataColumn(ft.Text("Planet 2")),
                ft.DataColumn(ft.Text("Angle")),
                ft.DataColumn(ft.Text("Aspect")),
                ft.DataColumn(ft.Text("Trend")),
            ],
            rows=[],
            border=ft.border.all(1, "grey400"),
            vertical_lines=ft.border.all(1, "grey400"),
            horizontal_lines=ft.border.all(1, "grey400"),
        )

    def update_data(self, aspects: list):
        self.rows = []
        for aspect in aspects:
            trend = aspect["trend"]
            # Color coding
            color = "black"
            if trend == "Positive":
                color = "green"
            elif trend == "Negative":
                color = "red"
            elif trend == "Neutral":
                color = "blue"

            self.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(aspect["planet1"])),
                        ft.DataCell(ft.Text(aspect["planet2"])),
                        ft.DataCell(ft.Text(f"{aspect['angle_deg']:.2f}°")),
                        ft.DataCell(ft.Text(aspect["aspect_name"])),
                        ft.DataCell(ft.Text(trend, color=color, weight=ft.FontWeight.BOLD)),
                    ]
                )
            )
        self.update()
