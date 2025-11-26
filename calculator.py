import math

# Default Aspect Rules
# Angle: (Name, Trend)
# We can use a dictionary where keys are the target angles.
DEFAULT_ASPECT_RULES = {
    0: {"name": "Conjunction", "trend": "Positive"},
    6: {"name": "Aspect 6", "trend": "Positive"},
    9: {"name": "Aspect 9", "trend": "Positive"},
    12: {"name": "Aspect 12", "trend": "Positive"},
    15: {"name": "Aspect 15", "trend": "Negative"},
    18: {"name": "Aspect 18", "trend": "Positive"},
    20: {"name": "Aspect 20", "trend": "Negative"},
    22.3: {"name": "Aspect 22.3", "trend": "Positive"},
    24: {"name": "Aspect 24", "trend": "Positive"},
    30: {"name": "Semi-Sextile", "trend": "Positive"},
    35: {"name": "Aspect 35", "trend": "Positive"},
    40: {"name": "Novile", "trend": "Positive"},
    45: {"name": "Semi-Square", "trend": "Negative"},
    60: {"name": "Sextile", "trend": "Positive"},
    72: {"name": "Quintile", "trend": "Positive"},
    90: {"name": "Square", "trend": "Negative"},
    120: {"name": "Trine", "trend": "Negative"},
    135: {"name": "Sesquiquadrate", "trend": "Positive"},
    144: {"name": "Biquintile", "trend": "Negative"},
    150: {"name": "Quincunx", "trend": "Positive"},
    180: {"name": "Opposition", "trend": "Negative"}
}

def calculate_aspects(positions: dict, rules: dict = None, orb: float = 3.0, specific_rules: list = None, range_rules: list = None):
    """
    Identifies aspects between all pairs of planets.
    
    Args:
        positions: dict {Planet: Degree}
        rules: dict {Angle: {name, trend}}
        orb: float, tolerance in degrees
        specific_rules: list of dicts [{p1, p2, angle, trend}]
        range_rules: list of dicts [{min, max, trend}]
        
    Returns:
        list of dicts: [{p1, p2, angle, aspect, trend, diff}]
    """
    if rules is None:
        rules = DEFAULT_ASPECT_RULES
    
    if specific_rules is None:
        specific_rules = []
        
    if range_rules is None:
        range_rules = []
        
    aspects_found = []
    planet_names = list(positions.keys())
    
    # Iterate unique pairs
    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1 = planet_names[i]
            p2 = planet_names[j]
            
            deg1 = positions[p1]
            deg2 = positions[p2]
            
            # Calculate angular difference (shortest distance on circle)
            diff = abs(deg1 - deg2)
            if diff > 180:
                diff = 360 - diff
                
            # Check against rules
            for target_angle, info in rules.items():
                # Check if diff is within orb of target_angle
                if abs(diff - float(target_angle)) <= orb:
                    
                    # Default Trend
                    trend = info["trend"]
                    
                    # 1. Check for Specific Rule Override (Highest Priority)
                    specific_override = False
                    for s_rule in specific_rules:
                        sp1 = s_rule.get("p1")
                        sp2 = s_rule.get("p2")
                        s_angle = s_rule.get("angle")
                        
                        planets_match = ({p1, p2} == {sp1, sp2})
                        angle_match = (s_angle == target_angle)
                        
                        if planets_match and angle_match:
                            trend = s_rule.get("trend")
                            specific_override = True
                            break
                    
                    # 2. Check for Range Rule Override (Medium Priority)
                    # Only if not overridden by specific rule
                    if not specific_override:
                        for r_rule in range_rules:
                            r_min = r_rule.get("min")
                            r_max = r_rule.get("max")
                            
                            if r_min <= diff <= r_max:
                                trend = r_rule.get("trend")
                                break
                    
                    aspects_found.append({
                        "planet1": p1,
                        "planet2": p2,
                        "angle_deg": diff,
                        "aspect_name": info["name"],
                        "trend": trend,
                        "orb_diff": abs(diff - float(target_angle)) # How exact it is
                    })
                    # Assuming only one aspect per pair (which is true for these standard angles)
                    break
                    
    return aspects_found

def calculate_planet_summary(aspects: list):
    """
    Calculate aspect summary statistics for each planet.
    
    Args:
        aspects: list of aspect dicts from calculate_aspects()
        
    Returns:
        dict: {planet_name: {total, positive, negative, neutral}}
    """
    summary = {}
    
    # Process each aspect
    for aspect in aspects:
        planet1 = aspect["planet1"]
        planet2 = aspect["planet2"]
        trend = aspect["trend"]
        
        # Initialize planet entries if not exists
        if planet1 not in summary:
            summary[planet1] = {"total": 0, "positive": 0, "negative": 0, "neutral": 0}
        if planet2 not in summary:
            summary[planet2] = {"total": 0, "positive": 0, "negative": 0, "neutral": 0}
        
        # Increment counts for both planets
        for planet in [planet1, planet2]:
            summary[planet]["total"] += 1
            
            if trend == "Positive":
                summary[planet]["positive"] += 1
            elif trend == "Negative":
                summary[planet]["negative"] += 1
            elif trend == "Neutral":
                summary[planet]["neutral"] += 1
    
    return summary
