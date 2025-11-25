import swisseph as swe
import datetime
import os

# Set Ephemeris path if needed, otherwise it uses default or built-in
# swe.set_ephe_path('/path/to/ephe')

def get_planetary_positions(dt: datetime.datetime, lat: float = 0.0, lon: float = 0.0):
    """
    Calculates sidereal planetary positions (Lahiri Ayanamsha) for a given datetime.
    
    Args:
        dt: datetime object (timezone aware or naive, if naive assumed UTC)
        lat: Latitude (observer) - not strictly needed for geocentric but good practice
        lon: Longitude (observer)
        
    Returns:
        dict: {PlanetName: Degree (0-360)}
    """
    
    # Set Sidereal Mode to Lahiri
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # Convert to Julian Day (ET)
    # If dt has timezone, convert to UTC first
    if dt.tzinfo:
        dt = dt.astimezone(datetime.timezone.utc)
    
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 + dt.second/3600.0)
    
    # Planets to calculate
    # Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (Mean Node), Ketu (Opposite Node)
    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE
    }
    
    results = {}
    
    for name, pid in planets.items():
        # flags: swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        # We use geocentric positions
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        
        # xx[0] is longitude
        xx, ret = swe.calc_ut(jd, pid, flags)
        
        results[name] = xx[0]
        
    # Calculate Ketu (Opposite of Rahu)
    ketu_pos = (results["Rahu"] + 180.0) % 360.0
    results["Ketu"] = ketu_pos
    
    return results

def format_degree(deg):
    """Converts decimal degree to DMS string or just rounded."""
    # For this app, decimal is fine for calculation, maybe string for display
    return f"{deg:.2f}"
