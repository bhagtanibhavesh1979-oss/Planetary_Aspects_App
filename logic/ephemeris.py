from astropy.time import Time
from astropy.coordinates import get_body, solar_system_ephemeris, GCRS
from astropy import units as u
import datetime
import numpy as np

# Use builtin ephemeris (no download needed)
solar_system_ephemeris.set('builtin')

# Lahiri ayanamsa calculation using exact Drik Panchang values
def get_ayanamsa(jd):
    """
    Calculate Lahiri ayanamsa for a given Julian Day
    Using exact values from Drik Panchang:
    - Base: 26° 36' 46.98" at 01-Jan-1900
    - Precession: 50.278650 seconds/year
    """
    # Convert base ayanamsa to decimal degrees
    # 26° 36' 46.98" = 26 + 36/60 + 46.98/3600
    base_ayanamsa_deg = 26.0 + 36.0/60.0 + 46.98/3600.0  # ≈ 26.6130500°
    
    # Precession rate in degrees per year
    precession_rate_deg_per_year = 50.278650 / 3600.0  # ≈ 0.01396629°/year
    
    # Julian Day for 01-Jan-1900, 00:00 UT
    jd_1900 = 2415020.5
    
    # Years since 1900
    years_since_1900 = (jd - jd_1900) / 365.25
    
    # Calculate current ayanamsa
    ayanamsa = base_ayanamsa_deg + (years_since_1900 * precession_rate_deg_per_year)
    
    return ayanamsa

def get_planetary_positions(dt: datetime.datetime, lat: float = 0.0, lon: float = 0.0):
    """
    Calculates sidereal planetary positions (Lahiri Ayanamsha) for a given datetime.
    
    Args:
        dt: datetime object (timezone aware or naive, if naive assumed UTC)
        lat: Latitude (observer)
        lon: Longitude (observer)
        
    Returns:
        dict: {PlanetName: Degree (0-360)}
    """
    
    # Convert to UTC if timezone aware
    if dt.tzinfo:
        dt = dt.astimezone(datetime.timezone.utc)
    
    # Create Astropy time object
    t = Time(dt)
    
    # Planet mapping
    planet_names = {
        'Sun': 'sun',
        'Moon': 'moon',
        'Mercury': 'mercury',
        'Venus': 'venus',
        'Mars': 'mars',
        'Jupiter': 'jupiter',
        'Saturn': 'saturn',
    }
    
    results = {}
    
    for name, body in planet_names.items():
        # Get geocentric position
        coord = get_body(body, t)
        
        # Convert to ecliptic coordinates (tropical)
        ecliptic_coord = coord.transform_to('geocentricmeanecliptic')
        tropical_lon = ecliptic_coord.lon.degree
        
        # Convert to sidereal using Lahiri ayanamsa
        jd = t.jd
        ayanamsa = get_ayanamsa(jd)
        sidereal_lon = (tropical_lon - ayanamsa) % 360.0
        
        results[name] = sidereal_lon
    
    # Calculate Rahu (North Node of Moon)
    jd = t.jd
    years_since_2000 = (jd - 2451545.0) / 365.25
    rahu_mean = (125.04 - years_since_2000 * 19.3) % 360.0
    results['Rahu'] = rahu_mean
    
    # Ketu is opposite to Rahu
    results['Ketu'] = (rahu_mean + 180.0) % 360.0
    
    return results

def format_degree(deg):
    """Converts decimal degree to DMS string or just rounded."""
    return f"{deg:.2f}"

