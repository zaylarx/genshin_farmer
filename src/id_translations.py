"""
ID to name translation mappings for Genshin Impact data.

This module provides mappings for translating numeric IDs to human-readable names.
Note: These are static mappings and may need updates as new content is added.

TODO: Find a way to hit the online json files rather than manually downloading them. (latter needs manual updating)
"""

# Character ID to Name mapping (from UID 657846809) - Verified from characters.json
CHARACTER_NAMES = {
    10000025: "Xingqiu",
    10000030: "Zhongli",
    10000031: "Fischl",
    10000046: "Hutao",  # Updated to match data file
    10000047: "Kazuha",  # Updated to match data file
    10000060: "Yelan",
    10000073: "Nahida",  # Fixed: was incorrectly "Baizhu"
    10000082: "Baizhu",  # Fixed: was incorrectly "Neuvillette" (file shows "Baizhuer")
    10000087: "Neuvillette",  # Fixed: was incorrectly "Furina"
    10000089: "Furina",  # Fixed: was incorrectly "Navia"
    10000103: "Xilonen",  # Fixed: was incorrectly "Chiori"
    10000123: "Durin",  # Fixed: was incorrectly "Arlecchino"
}

# Artifact Set ID to Name mapping (from UID 657846809)
ARTIFACT_SETS = {
    15001: "Gladiator's Finale",
    15002: "Deepwood Memories",
    15003: "Gilded Dreams",
    15006: "Crimson Witch of Flames",
    15007: "Shimenawa's Reminiscence",
    15017: "Tenacity of the Millelith",
    15019: "Pale Flame",
    15020: "Heart of Depth",
    15025: "Vourukasha's Glow",
    15026: "Nighttime Whispers in the Echoing Woods",
    15028: "Song of Days Past",
    15031: "Marechaussee Hunter",
    15032: "Golden Troupe",
    15037: "Fragment of Harmonic Whimsy",
}

# Weapon ID to Name mapping (from UID 657846809) - Verified from WeaponExcelConfigData.json
WEAPON_NAMES = {
    11401: "Favonius Sword",        # Sword_Zephyrus
    11403: "Sacrificial Sword",     # Sword_Fossil
    11422: "Lion's Roar",           # Sword_Kasabouzu
    11424: "The Flute",             # Sword_Boreas
    11426: "Iron Sting",            # Sword_Machination
    13303: "Sacrificial Lance",     # Pole_Noire (WEAPON_POLE, not greatsword!)
    13501: "Staff of Homa",         # Pole_Homa
    14403: "Sacrificial Fragments", # Catalyst_Fossil (not Favonius Lance!)
    14406: "Prototype Amber",       # Catalyst_Proto (not The Catch!)
    14424: "The Widsith",           # Catalyst_Yue (was incorrectly on 15409!)
    15401: "Favonius Warbow",       # Bow_Zephyrus (not Codex!)
    15409: "The Viridescent Hunt",  # Bow_Viridescent (not Widsith!)
}

# Fight Prop numeric keys to readable names
FIGHT_PROP_NAMES = {
    "1": "HP",
    "2": "ATK",
    "3": "DEF",
    "4": "HP%",
    "5": "ATK%",
    "6": "DEF%",
    "7": "Elemental Mastery",
    "8": "Energy Recharge",
    "9": "CRIT Rate",
    "20": "CRIT DMG",
    "22": "Healing Bonus",
    "23": "Incoming Healing Bonus",
    "26": "Elemental DMG Bonus",
    "27": "Physical DMG Bonus",
    "28": "Elemental Mastery",
    "40": "Pyro DMG Bonus",
    "41": "Electro DMG Bonus",
    "42": "Hydro DMG Bonus",
    "43": "Dendro DMG Bonus",
    "44": "Anemo DMG Bonus",
    "45": "Geo DMG Bonus",
    "46": "Cryo DMG Bonus",
    "50": "Pyro RES",
    "51": "Electro RES",
    "52": "Hydro RES",
    "53": "Dendro RES",
    "54": "Anemo RES",
    "55": "Geo RES",
    "56": "Cryo RES",
}

# Main Prop ID to name mapping (for artifacts)
MAIN_PROP_NAMES = {
    14001: "HP",
    12001: "ATK",
    10001: "DEF",
    10002: "HP%",
    10003: "ATK%",
    10004: "DEF%",
    10005: "Elemental Mastery",
    10006: "DEF%",
    10007: "Energy Recharge",
    10008: "Elemental Mastery",
    13001: "CRIT Rate",
    13002: "CRIT DMG",
    13003: "Healing Bonus",
    13007: "CRIT Rate",
    13008: "CRIT DMG",
    13010: "Elemental Mastery",
    15001: "Pyro DMG Bonus",
    15002: "Electro DMG Bonus",
    15003: "Hydro DMG Bonus",
    15004: "Dendro DMG Bonus",
    15005: "Anemo DMG Bonus",
    15006: "Geo DMG Bonus",
    15007: "Cryo DMG Bonus",
    15008: "Pyro DMG Bonus",
    15009: "Electro DMG Bonus",
    15011: "Hydro DMG Bonus",
    15014: "Dendro DMG Bonus",
}

# Elemental DMG Bonus mapping (for goblets)
ELEMENTAL_DMG_BONUS = {
    15001: "Pyro DMG Bonus",
    15002: "Electro DMG Bonus",
    15003: "Hydro DMG Bonus",
    15004: "Dendro DMG Bonus",
    15005: "Anemo DMG Bonus",
    15006: "Geo DMG Bonus",
    15007: "Cryo DMG Bonus",
    15008: "Pyro DMG Bonus",
    15009: "Electro DMG Bonus",
    15011: "Hydro DMG Bonus",
    15014: "Dendro DMG Bonus",
}


def get_character_name(avatar_id: int) -> str:
    """Get character name from avatar ID."""
    return CHARACTER_NAMES.get(avatar_id, f"Character {avatar_id}")


def get_artifact_set_name(set_id: int) -> str:
    """Get artifact set name from set ID."""
    return ARTIFACT_SETS.get(set_id, f"Set {set_id}")


def get_fight_prop_name(prop_key: str) -> str:
    """Get readable name for fight prop numeric key."""
    return FIGHT_PROP_NAMES.get(prop_key, f"Prop {prop_key}")


def get_main_prop_name(prop_id: int) -> str:
    """Get readable name for artifact main stat prop ID."""
    # Check elemental DMG bonus first
    if prop_id in ELEMENTAL_DMG_BONUS:
        return ELEMENTAL_DMG_BONUS[prop_id]
    return MAIN_PROP_NAMES.get(prop_id, f"Prop {prop_id}")


def get_weapon_name(weapon_id: int) -> str:
    """Get weapon name from weapon ID."""
    return WEAPON_NAMES.get(weapon_id, f"Weapon {weapon_id}")


def get_stat_name(stat_id: str) -> str:
    """Get readable name for stat ID (handles both FIGHT_PROP_* and numeric keys)."""
    # If it's already a readable name like "FIGHT_PROP_HP", clean it up
    if stat_id.startswith("FIGHT_PROP_"):
        # Remove prefix and convert to readable format
        name = stat_id.replace("FIGHT_PROP_", "")
        # Convert underscores to spaces and title case
        name = name.replace("_", " ").title()
        # Handle special cases
        name = name.replace("Hp", "HP").replace("Atk", "ATK").replace("Def", "DEF")
        name = name.replace("Crit", "CRIT").replace("Crit Hurt", "CRIT DMG")
        name = name.replace("Base Attack", "Base ATK")
        name = name.replace("Charge Efficiency", "Energy Recharge")
        name = name.replace("Element Mastery", "Elemental Mastery")
        name = name.replace("Fire Add Hurt", "Pyro DMG Bonus")
        name = name.replace("Water Add Hurt", "Hydro DMG Bonus")
        name = name.replace("Grass Add Hurt", "Dendro DMG Bonus")
        name = name.replace("Elec Add Hurt", "Electro DMG Bonus")
        name = name.replace("Wind Add Hurt", "Anemo DMG Bonus")
        name = name.replace("Rock Add Hurt", "Geo DMG Bonus")
        name = name.replace("Ice Add Hurt", "Cryo DMG Bonus")
        return name
    # Otherwise try numeric key
    return get_fight_prop_name(stat_id)

