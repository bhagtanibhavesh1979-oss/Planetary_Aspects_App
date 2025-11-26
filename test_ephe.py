from pymeeus.Sun import Sun
from pymeeus.Moon import Moon
from pymeeus.Mercury import Mercury
from pymeeus.Venus import Venus
from pymeeus.Mars import Mars
from pymeeus.Jupiter import Jupiter
from pymeeus.Saturn import Saturn
from pymeeus.Epoch import Epoch
from pymeeus.Coordinates import equatorial2ecliptical, true_obliquity
import datetime

# Lahiri ayanamsa calculation using exact Drik Panchang values
def get_ayanamsa(jd):
    """
    Calculate Lahiri ayanamsa for a given Julian Day
    Using exact values from Drik Panchang:
    - Base: 26° 36' 46.98" at 01-Jan-1900
    - Precession: 50.278650 seconds/year
    """
    # Convert base ayanamsa to decimal degrees
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
    
    # Create PyMeeus Epoch object
    epoch = Epoch(dt.year, dt.month, dt.day + dt.hour/24.0 + dt.minute/1440.0 + dt.second/86400.0)
    
    # Get Julian Day
    jd = epoch.jde()
    
    # Calculate ayanamsa
    ayanamsa = get_ayanamsa(jd)
    
    # Get obliquity of ecliptic for coordinate conversion
    epsilon = true_obliquity(epoch)
    
    results = {}
    
    # Sun - Uses apparent_geocentric_position which returns ecliptical coords
    sun_lon, sun_lat, sun_dist = Sun.apparent_geocentric_position(epoch)
    results['Sun'] = (float(sun_lon) - ayanamsa) % 360.0
    
    # Moon - Returns 4 values: (lon, lat, dist, parallax) already in ecliptical coords
    moon_lon, moon_lat, moon_dist, moon_parallax = Moon.apparent_ecliptical_pos(epoch)
    results['Moon'] = (float(moon_lon) - ayanamsa) % 360.0
    
    # Mercury - geocentric_position returns equatorial (RA/Dec), convert to ecliptical
    ra, dec, dist = Mercury.geocentric_position(epoch)
    mercury_lon, mercury_lat = equatorial2ecliptical(ra, dec, epsilon)
    results['Mercury'] = (float(mercury_lon) - ayanamsa) % 360.0
    
    # Venus
    ra, dec, dist = Venus.geocentric_position(epoch)
    venus_lon, venus_lat = equatorial2ecliptical(ra, dec, epsilon)
    results['Venus'] = (float(venus_lon) - ayanamsa) % 360.0
    
    # Mars
    ra, dec, dist = Mars.geocentric_position(epoch)
    mars_lon, mars_lat = equatorial2ecliptical(ra, dec, epsilon)
    results['Mars'] = (float(mars_lon) - ayanamsa) % 360.0
    
    # Jupiter
    ra, dec, dist = Jupiter.geocentric_position(epoch)
    jupiter_lon, jupiter_lat = equatorial2ecliptical(ra, dec, epsilon)
    results['Jupiter'] = (float(jupiter_lon) - ayanamsa) % 360.0
    
    # Saturn
    ra, dec, dist = Saturn.geocentric_position(epoch)


