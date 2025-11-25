try:
    import swisseph as swe
    print("Imported swisseph successfully")
    print(f"Swe Version: {swe.version()}")
except Exception as e:
    print(f"Error importing swisseph: {e}")
