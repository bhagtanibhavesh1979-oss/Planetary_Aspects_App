import datetime
from logic.ephemeris import get_planetary_positions
from logic.calculator import calculate_aspects, DEFAULT_ASPECT_RULES

def test_logic():
    print("Testing Logic...")
    
    # 1. Test Ephemeris
    now = datetime.datetime.now()
    print(f"Current Time: {now}")
    try:
        positions = get_planetary_positions(now)
        print("Planetary Positions (Sidereal Lahiri):")
        for p, d in positions.items():
            print(f"  {p}: {d:.2f}")
    except Exception as e:
        print(f"Ephemeris Error: {e}")
        return

    # 2. Test Calculator
    print("\nTesting Aspect Calculator...")
    # Create a fake scenario for testing aspects
    # Sun at 0, Moon at 120 (Trine), Mars at 90 (Square)
    fake_positions = {
        "Sun": 0.0,
        "Moon": 120.0,
        "Mars": 90.0,
        "Venus": 10.0 # No aspect
    }
    
    aspects = calculate_aspects(fake_positions, DEFAULT_ASPECT_RULES, orb=3.0)
    print(f"Found {len(aspects)} aspects (Expected ~2):")
    for a in aspects:
        print(f"  {a['planet1']} - {a['planet2']}: {a['angle_deg']:.2f} ({a['aspect_name']} - {a['trend']})")
        
    # Check if we found the expected ones
    has_trine = any(a['aspect_name'] == 'Trine' for a in aspects)
    has_square = any(a['aspect_name'] == 'Square' for a in aspects)
    
    if has_trine and has_square:
        print("\nSUCCESS: Logic verification passed!")
    else:
        print("\nFAILURE: Logic verification failed!")

if __name__ == "__main__":
    test_logic()
