import flet as ft
import datetime
from logic.ephemeris import get_planetary_positions
from logic.calculator import calculate_aspects, DEFAULT_ASPECT_RULES
from ui.app_layout import AppLayout

def main(page: ft.Page):
    page.title = "Planetary Aspects App"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # State
    current_orb = 3.0
    current_rules = DEFAULT_ASPECT_RULES.copy()
    current_specific_rules = []
    current_range_rules = []
    current_date = None # None means Now
    current_time = None
    current_planet_filter = "All"
    
    def update_ui(orb, rules, specific_rules, range_rules, date, time, planet_filter):
        nonlocal current_orb, current_rules, current_specific_rules, current_range_rules, current_date, current_time, current_planet_filter
        current_orb = orb
        current_rules = rules
        current_specific_rules = specific_rules
        current_range_rules = range_rules
        current_date = date
        current_time = time
        current_planet_filter = planet_filter
        
        # 1. Get Positions
        # If date is None, use now. If date is set, use that date
        if current_date:
            # If time is provided, use it, otherwise default to 12:00
            t = current_time if current_time else datetime.time(12, 0)
            calc_date = datetime.datetime.combine(current_date, t)
        else:
            calc_date = datetime.datetime.now()
            
        positions = get_planetary_positions(calc_date)
        
        # 2. Calculate Aspects
        aspects = calculate_aspects(positions, current_rules, current_orb, current_specific_rules, current_range_rules)
        
        # 3. Filter Aspects
        if current_planet_filter and current_planet_filter != "All":
            filtered_aspects = [
                a for a in aspects 
                if a["planet1"] == current_planet_filter or a["planet2"] == current_planet_filter
            ]
        else:
            filtered_aspects = aspects

        # 4. Update Tables
        app_layout.positions_table.update_data(positions)
        app_layout.aspects_table.update_data(filtered_aspects)
        
        # 5. Check for Alerts (Simple SnackBar for now)
        # Filter for very close aspects (e.g., < 1 deg)
        close_aspects = [a for a in filtered_aspects if a["orb_diff"] < 1.0]
        if close_aspects:
            msg = f"Alert: {len(close_aspects)} close aspects found!"
            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True
            page.update()

    # Initialize Layout
    app_layout = AppLayout(
        on_settings_change=update_ui,
        default_orb=current_orb,
        default_rules=current_rules,
        default_specific_rules=current_specific_rules,
        default_range_rules=current_range_rules
    )
    
    # Add Pickers to page overlay
    page.overlay.append(app_layout.settings_sidebar.date_picker)
    page.overlay.append(app_layout.settings_sidebar.time_picker)
    
    page.add(app_layout)
    
    # Initial Calculation
    update_ui(current_orb, current_rules, current_specific_rules, current_range_rules, current_date, current_time, current_planet_filter)

if __name__ == "__main__":
    ft.app(target=main)
