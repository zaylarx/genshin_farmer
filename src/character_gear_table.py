"""
Display character artifact information in a table format.

Takes a character name as argument and shows main stat + substats for each artifact.
"""

import asyncio
import sys
import pandas as pd
from typing import Dict, List, Optional
from fetch_player_info_direct import (
    fetch_player_data,
    EnkaNetworkResponse,
    ReliquaryFlat,
)
from id_translations import (
    get_character_name,
    get_stat_name
)


# Artifact equipment type mapping
ARTIFACT_TYPE_NAMES = {
    "EQUIP_BRACER": "Flower",
    "EQUIP_NECKLACE": "Plume", 
    "EQUIP_SHOES": "Sands",
    "EQUIP_RING": "Goblet",
    "EQUIP_DRESS": "Circlet",
}


def find_character(data: EnkaNetworkResponse, character_name: str):
    """
    Find a character by name in the player's data.
    
    Args:
        data: Player data from Enka Network
        character_name: Name of the character to find (case-insensitive)
        
    Returns:
        Character info if found, None otherwise
    """
    character_name_lower = character_name.lower()
    
    for char in data.avatarInfoList:
        char_name = get_character_name(char.avatarId)
        if char_name.lower() == character_name_lower:
            return char
    
    return None


def extract_artifact_details(character) -> List[Dict]:
    """
    Extract artifact details for a character.
    
    Returns:
        List of dictionaries containing artifact info (one per artifact piece)
    """
    artifacts = []
    
    # Process equipment
    for equip in character.equipList:
        if equip.reliquary:
            flat = equip.flat
            if isinstance(flat, ReliquaryFlat):
                # Determine artifact slot
                equip_type = flat.equipType
                slot_name = ARTIFACT_TYPE_NAMES.get(equip_type, "Unknown")
                
                artifact_info = {
                    "Artifact": slot_name,
                    "Main Stat": None,
                    "Substat 1": None,
                    "Substat 2": None,
                    "Substat 3": None,
                    "Substat 4": None,
                }
                
                # Get main stat
                if flat.reliquaryMainstat:
                    stat_name = get_stat_name(flat.reliquaryMainstat.mainPropId)
                    stat_value = flat.reliquaryMainstat.statValue
                    if isinstance(stat_value, float) and stat_value < 100:
                        artifact_info["Main Stat"] = f"{stat_name} {stat_value:.1f}%"
                    else:
                        artifact_info["Main Stat"] = f"{stat_name} {stat_value:.0f}"
                
                # Get substats
                if flat.reliquarySubstats:
                    for i, substat in enumerate(flat.reliquarySubstats, 1):
                        if i <= 4:  # Only take first 4 substats
                            substat_name = get_stat_name(substat.appendPropId)
                            stat_value = substat.statValue
                            if isinstance(stat_value, float) and stat_value < 100:
                                substat_str = f"{substat_name} {stat_value:.1f}%"
                            else:
                                substat_str = f"{substat_name} {stat_value:.0f}"
                            artifact_info[f"Substat {i}"] = substat_str
                
                artifacts.append(artifact_info)
    
    # Sort by artifact order
    artifact_order = ["Flower", "Plume", "Sands", "Goblet", "Circlet"]
    artifacts.sort(key=lambda x: artifact_order.index(x["Artifact"]) if x["Artifact"] in artifact_order else 999)
    
    return artifacts


def create_artifact_table(character, character_name: str) -> pd.DataFrame:
    """
    Create a pandas DataFrame with artifact information.
    
    Args:
        character: Character data
        character_name: Name of the character
        
    Returns:
        DataFrame with artifact details
    """
    artifacts = extract_artifact_details(character)
    df = pd.DataFrame(artifacts)
    
    return df


def display_artifact_table(df: pd.DataFrame, character_name: str):
    """Display the artifact table in a readable format."""
    print("\n" + "=" * 120)
    print(f"ARTIFACTS FOR {character_name.upper()}")
    print("=" * 120)
    
    # Configure pandas display options for better readability
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 25)
    
    print(df.to_string(index=False))
    print("=" * 120)


def export_to_csv(df: pd.DataFrame, character_name: str, filename: str = None):
    """Export the artifact table to CSV."""
    if filename is None:
        filename = f"{character_name.lower()}_artifacts.csv"
    df.to_csv(filename, index=False)
    print(f"\nArtifact table exported to '{filename}'")


async def main():
    """Main function."""
    # Check if character name argument was provided
    if len(sys.argv) < 2:
        print("Usage: python character_gear_table.py <character_name>")
        print("Example: python character_gear_table.py Furina")
        sys.exit(1)
    
    character_name = sys.argv[1]
    uid = 657846809
    
    print(f"Fetching player information for UID: {uid}")
    print(f"Looking for character: {character_name}")
    print("=" * 70)
    
    data = await fetch_player_data(uid)
    
    if not data:
        print("\n[ERROR] Failed to fetch or parse player data")
        sys.exit(1)
    
    # Find the character
    character = find_character(data, character_name)
    
    if not character:
        print(f"\n[ERROR] Character '{character_name}' not found in UID {uid}")
        print("\nAvailable characters:")
        for char in data.avatarInfoList:
            print(f"  - {get_character_name(char.avatarId)}")
        sys.exit(1)
    
    print(f"[SUCCESS] Found character: {character_name}")
    
    # Create artifact table
    df = create_artifact_table(character, character_name)
    
    # Display table
    display_artifact_table(df, character_name)
    
    # Export to CSV
    export_to_csv(df, character_name)


if __name__ == "__main__":
    asyncio.run(main())
