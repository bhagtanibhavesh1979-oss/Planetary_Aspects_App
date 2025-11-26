import flet as ft
import json
import datetime
from logic.calculator import DEFAULT_ASPECT_RULES

class SettingsSidebar(ft.Column):
    def __init__(self, on_change_callback, default_orb=3.0, default_rules=None, default_specific_rules=None, default_range_rules=None):
        super().__init__()
        self.on_change_callback = on_change_callback
        self.width = 300
        self.spacing = 20
        self.scroll = ft.ScrollMode.AUTO
        
        # Initialize specific rules list
        self.specific_rules_list = default_specific_rules if default_specific_rules else []
        
        # Date Picker
        self.date_picker = ft.DatePicker(
            on_change=self.trigger_change,
        )
        
        # Time Picker
        self.time_picker = ft.TimePicker(
            on_change=self.trigger_change,
            value=datetime.time(12, 0) # Default to noon
        )
        
        self.date_button = ft.ElevatedButton(
            "Pick Date",
            icon="calendar_month",
            on_click=self.open_date_picker
        )
        self.selected_date_text = ft.Text("Current: Today")

        self.time_button = ft.ElevatedButton(
            "Pick Time",
            icon="access_time",
            on_click=self.open_time_picker
        )
        self.selected_time_text = ft.Text("Time: 12:00:00")

        # Planet Filter (Moved to Top)
        self.planet_filter = ft.Dropdown(
            label="Filter by Planet",
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("Sun"),
                ft.dropdown.Option("Moon"),
                ft.dropdown.Option("Mars"),
                ft.dropdown.Option("Mercury"),
                ft.dropdown.Option("Jupiter"),
                ft.dropdown.Option("Venus"),
                ft.dropdown.Option("Saturn"),
                ft.dropdown.Option("Rahu"),
                ft.dropdown.Option("Ketu")
            ],
            value="All",
            on_change=self.trigger_change
        )

        self.orb_input = ft.TextField(
            label="Orb Tolerance (deg)", 
            value=str(default_orb), 
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.trigger_change
        )
        
        # Format default rules as JSON string
        rules_str = json.dumps(default_rules, indent=2) if default_rules else "{}"
        
        self.rules_input = ft.TextField(
            label="Aspect Rules (JSON)",
            value=rules_str,
            multiline=True,
            min_lines=5,
            max_lines=10,
            text_size=12,
            on_change=self.trigger_change
        )
        
        # --- Specific Rule Builder ---
        self.p1_dropdown = ft.Dropdown(
            label="Planet 1",
            options=[ft.dropdown.Option(p) for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]],
            width=130,
            text_size=12
        )
        self.p2_dropdown = ft.Dropdown(
            label="Planet 2",
            options=[ft.dropdown.Option(p) for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]],
            width=130,
            text_size=12
        )
        
        # Populate angles from DEFAULT_ASPECT_RULES
        sorted_angles = sorted(DEFAULT_ASPECT_RULES.keys())
        self.angle_dropdown = ft.Dropdown(
            label="Angle",
            options=[ft.dropdown.Option(str(a)) for a in sorted_angles],
            width=130,
            text_size=12
        )
        
        self.trend_dropdown = ft.Dropdown(
            label="Trend",
            options=[
                ft.dropdown.Option("Positive"),
                ft.dropdown.Option("Negative"),
                ft.dropdown.Option("Neutral")
            ],
            width=130,
            text_size=12
        )
        
        self.add_rule_btn = ft.ElevatedButton("Add Rule", on_click=self.add_specific_rule)
        self.rules_list_view = ft.Column()
        self.update_rules_list_view(update_control=False)

        # Range Rules
        range_rules_str = json.dumps(default_range_rules, indent=2) if default_range_rules else "[]"
        self.range_rules_input = ft.TextField(
            label="Degree Range Rules (JSON)",
            value=range_rules_str,
            multiline=True,
            min_lines=3,
            max_lines=6,
            text_size=12,
            on_change=self.trigger_change
        )
        
        self.error_text = ft.Text("", color="red")

        self.controls = [
            ft.Text("Settings", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Date & Time:"),
            ft.Row([self.date_button, self.time_button]),
            self.selected_date_text,
            self.selected_time_text,
            ft.Row([
                ft.ElevatedButton("-15m", on_click=lambda e: self.adjust_time(-15)),
                ft.ElevatedButton("+15m", on_click=lambda e: self.adjust_time(15))
            ]),
            ft.Divider(),
            self.planet_filter, # Moved to top
            ft.Divider(),
            self.orb_input,
            # ft.Text("General Rules (JSON):"),
            # self.rules_input,
            # ft.Divider(),
            # ft.Text("Specific Pair Rules:", weight=ft.FontWeight.BOLD),
            # ft.Row([self.p1_dropdown, self.p2_dropdown]),
            # ft.Row([self.angle_dropdown, self.trend_dropdown]),
            # self.add_rule_btn,
            # self.rules_list_view,
            # ft.Divider(),
            # ft.Text("Degree Range Rules (JSON):"),
            # ft.Text('Example: [{"min":0,"max":1,"trend":"Positive"}]', size=10, italic=True),
            # self.range_rules_input,
            self.error_text
        ]

    def open_date_picker(self, e):
        self.date_picker.open = True
        self.date_picker.update()

    def open_time_picker(self, e):
        self.time_picker.open = True
        self.time_picker.update()

    def adjust_time(self, minutes):
        current_time = self.time_picker.value if self.time_picker.value else datetime.time(12, 0)
        dt = datetime.datetime.combine(datetime.date.today(), current_time)
        dt += datetime.timedelta(minutes=minutes)
        self.time_picker.value = dt.time()
        self.trigger_change(None)
        
    def add_specific_rule(self, e):
        p1 = self.p1_dropdown.value
        p2 = self.p2_dropdown.value
        angle_str = self.angle_dropdown.value
        trend = self.trend_dropdown.value
        
        if not all([p1, p2, angle_str, trend]):
            self.error_text.value = "Please select all fields for the rule."
            self.error_text.update()
            return

        try:
            angle = float(angle_str)
        except ValueError:
            self.error_text.value = "Invalid angle."
            self.error_text.update()
            return
            
        # Add to list
        new_rule = {"p1": p1, "p2": p2, "angle": angle, "trend": trend}
        self.specific_rules_list.append(new_rule)
        
        # Clear inputs
        self.p1_dropdown.value = None
        self.p2_dropdown.value = None
        self.angle_dropdown.value = None
        self.trend_dropdown.value = None
        
        self.update_rules_list_view()
        self.trigger_change(None)
        
    def delete_rule(self, index):
        if 0 <= index < len(self.specific_rules_list):
            self.specific_rules_list.pop(index)
            self.update_rules_list_view()
            self.trigger_change(None)

    def update_rules_list_view(self, update_control=True):
        items = []
        for i, rule in enumerate(self.specific_rules_list):
            items.append(
                ft.Row([
                    ft.Text(f"{rule['p1']} - {rule['p2']} @ {rule['angle']}° : {rule['trend']}", size=12),
                    ft.IconButton(ft.icons.DELETE, size=20, on_click=lambda e, idx=i: self.delete_rule(idx))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        self.rules_list_view.controls = items
        if update_control:
            self.rules_list_view.update()
    
    def trigger_change(self, e):
        # Update Date Text
        if self.date_picker.value:
            self.selected_date_text.value = f"Date: {self.date_picker.value.strftime('%Y-%m-%d')}"
        else:
            self.selected_date_text.value = "Date: Today (Live)"
        self.selected_date_text.update()

        # Update Time Text
        if self.time_picker.value:
            self.selected_time_text.value = f"Time: {self.time_picker.value.strftime('%H:%M:%S')}"
        else:
            self.selected_time_text.value = "Time: 12:00:00"
        self.selected_time_text.update()

        # Validate inputs
        try:
            orb = float(self.orb_input.value)
            rules = json.loads(self.rules_input.value)
            # specific_rules is now self.specific_rules_list
            range_rules = json.loads(self.range_rules_input.value)
            
            self.error_text.value = ""
            self.error_text.update()
            
            # Convert keys to float for the logic layer (supports 22.3 etc)
            converted_rules = {}
            for k, v in rules.items():
                converted_rules[float(k)] = v
            
            # Callback with new signature
            self.on_change_callback(
                orb, 
                converted_rules, 
                self.specific_rules_list, 
                range_rules, 
                self.date_picker.value,
                self.time_picker.value,
                self.planet_filter.value
            )
            
        except ValueError:
            self.error_text.value = "Invalid Orb value"
            self.error_text.update()
        except json.JSONDecodeError:
            self.error_text.value = "Invalid JSON format"
            self.error_text.update()
        except Exception as ex:
            self.error_text.value = f"Error: {str(ex)}"
            self.error_text.update()
