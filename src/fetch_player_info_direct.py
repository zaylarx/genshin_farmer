"""
Fetch Genshin Impact player information directly from Enka Network API.

This script makes direct API calls and uses Pydantic models based on the
actual API response structure from https://api.enka.network/
"""

import asyncio
import aiohttp
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from id_translations import (
    get_character_name,
    get_artifact_set_name,
    get_fight_prop_name,
    get_main_prop_name,
    get_stat_name,
    get_weapon_name
)


# ============================================================================
# Pydantic Models based on actual API response structure
# ============================================================================

class ProfilePicture(BaseModel):
    id: int


class ShowAvatarInfo(BaseModel):
    avatarId: int  # API returns int, not string
    level: int
    energyType: int
    costumeId: Optional[int] = None


class PlayerInfo(BaseModel):
    nickname: str
    level: int
    worldLevel: int
    nameCardId: int
    finishAchievementNum: int
    towerFloorIndex: int
    towerLevelIndex: int
    showAvatarInfoList: List[ShowAvatarInfo]
    profilePicture: ProfilePicture
    theaterActIndex: Optional[int] = None
    theaterModeIndex: Optional[int] = None
    theaterStarIndex: Optional[int] = None
    fetterCount: Optional[int] = None
    towerStarIndex: Optional[int] = None
    stygianIndex: Optional[int] = None
    stygianSeconds: Optional[int] = None
    stygianId: Optional[int] = None


class ReliquarySubstat(BaseModel):
    appendPropId: str
    statValue: Union[int, float]  # Can be int or float (e.g., 10.2, 35, 7.4)


class ReliquaryMainstat(BaseModel):
    mainPropId: str
    statValue: Union[int, float]  # Can be int or float


class ReliquaryFlat(BaseModel):
    nameTextMapHash: str
    rankLevel: int
    itemType: str
    icon: str
    equipType: str
    setId: Optional[int] = None
    setNameTextMapHash: Optional[str] = None
    reliquarySubstats: Optional[List[ReliquarySubstat]] = None
    reliquaryMainstat: Optional[ReliquaryMainstat] = None


class Reliquary(BaseModel):
    level: int
    mainPropId: int
    appendPropIdList: List[int]


class WeaponStat(BaseModel):
    appendPropId: str
    statValue: Union[int, float]  # Can be int or float (e.g., 608, 66.2)


class WeaponFlat(BaseModel):
    nameTextMapHash: str
    rankLevel: int
    itemType: str
    icon: str
    weaponStats: List[WeaponStat]


class Weapon(BaseModel):
    level: int
    promoteLevel: int
    affixMap: Dict[str, int]


class Equipment(BaseModel):
    itemId: int
    reliquary: Optional[Reliquary] = None
    weapon: Optional[Weapon] = None
    flat: Union[ReliquaryFlat, WeaponFlat]  # Can be either type


class FetterInfo(BaseModel):
    expLevel: int


class AvatarInfo(BaseModel):
    avatarId: int
    propMap: Dict[str, Dict[str, Any]]
    talentIdList: Optional[List[int]] = None  # Optional - not all characters have this
    fightPropMap: Dict[str, float]
    skillDepotId: int
    inherentProudSkillList: List[int]
    skillLevelMap: Dict[str, int]
    equipList: List[Equipment]
    fetterInfo: FetterInfo


class EnkaNetworkResponse(BaseModel):
    playerInfo: PlayerInfo
    avatarInfoList: List[AvatarInfo]
    ttl: int
    uid: str


# ============================================================================
# API Client
# ============================================================================

async def fetch_player_data(uid: int) -> Optional[EnkaNetworkResponse]:
    """
    Fetch player data from Enka Network API.
    
    Args:
        uid: Genshin Impact player UID
        
    Returns:
        Parsed EnkaNetworkResponse or None if error
    """
    url = f"https://enka.network/api/uid/{uid}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Parse with Pydantic models
                    return EnkaNetworkResponse(**data)
                else:
                    print(f"API returned status {response.status}")
                    text = await response.text()
                    print(f"Response: {text}")
                    return None
    except Exception as e:
        print(f"Error fetching data: {type(e).__name__}: {e}")
        return None


# ============================================================================
# Display Functions
# ============================================================================

def display_player_info(data: EnkaNetworkResponse):
    """Display player profile information."""
    player = data.playerInfo
    
    print("\n=== PROFILE INFORMATION ===")
    print(f"Nickname: {player.nickname}")
    print(f"Level: {player.level}")
    print(f"World Level: {player.worldLevel}")
    print(f"Achievements: {player.finishAchievementNum}")
    print(f"Abyss Floor: {player.towerFloorIndex}-{player.towerLevelIndex}")
    
    print(f"\nShowcase Characters ({len(player.showAvatarInfoList)}):")
    for i, avatar in enumerate(player.showAvatarInfoList, 1):
        char_name = get_character_name(avatar.avatarId)
        print(f"  {i}. {char_name} (ID: {avatar.avatarId}), Level: {avatar.level}")


def display_character_info(data: EnkaNetworkResponse):
    """Display detailed character information."""
    print(f"\n=== CHARACTERS ({len(data.avatarInfoList)} total) ===")
    
    for i, char in enumerate(data.avatarInfoList, 1):
        char_name = get_character_name(char.avatarId)
        print(f"\n--- Character {i}: {char_name} (ID: {char.avatarId}) ---")
        print(f"  Skill Depot ID: {char.skillDepotId}")
        print(f"  Friendship Level: {char.fetterInfo.expLevel}")
        if char.talentIdList:
            print(f"  Constellations: {len(char.talentIdList)} unlocked")
        else:
            print(f"  Constellations: None")
        
        # Display stats from fightPropMap
        if "1" in char.fightPropMap:
            print(f"  HP: {char.fightPropMap['1']:.0f}")
        if "2" in char.fightPropMap:
            print(f"  ATK: {char.fightPropMap['2']:.0f}")
        if "3" in char.fightPropMap:
            print(f"  DEF: {char.fightPropMap['3']:.0f}")
        if "20" in char.fightPropMap:
            print(f"  CRIT Rate: {char.fightPropMap['20']*100:.1f}%")
        if "22" in char.fightPropMap:
            print(f"  CRIT DMG: {char.fightPropMap['22']*100:.1f}%")
        
        # Display equipment
        print(f"  Equipment ({len(char.equipList)} items):")
        for equip in char.equipList:
            if equip.reliquary:
                # Artifact
                flat = equip.flat
                if isinstance(flat, ReliquaryFlat):
                    # Get artifact set name
                    set_name = ""
                    if flat.setId:
                        set_name = f" ({get_artifact_set_name(flat.setId)})"
                    
                    # Get main stat name
                    if flat.reliquaryMainstat:
                        mainstat = flat.reliquaryMainstat
                        mainstat_name = get_stat_name(mainstat.mainPropId)
                        # Format stat value (add % for percentages)
                        stat_value = mainstat.statValue
                        if isinstance(stat_value, float) and stat_value < 100:
                            stat_display = f"{stat_value:.1f}%"
                        else:
                            stat_display = f"{stat_value:.0f}"
                        print(f"    Artifact{set_name}: {mainstat_name} = {stat_display}")
                    
                    # Display substats
                    if flat.reliquarySubstats:
                        for substat in flat.reliquarySubstats:
                            substat_name = get_stat_name(substat.appendPropId)
                            # Format stat value
                            stat_value = substat.statValue
                            if isinstance(stat_value, float) and stat_value < 100:
                                stat_display = f"{stat_value:.1f}%"
                            else:
                                stat_display = f"{stat_value:.0f}"
                            print(f"      {substat_name}: {stat_display}")
            elif equip.weapon:
                # Weapon
                flat = equip.flat
                if isinstance(flat, WeaponFlat):
                    weapon_name = get_weapon_name(equip.itemId)
                    refinement = max(equip.weapon.affixMap.values()) + 1 if equip.weapon.affixMap else 1
                    print(f"    {weapon_name}: Level {equip.weapon.level}, Refinement R{refinement}")
                    for stat in flat.weaponStats:
                        stat_name = get_stat_name(stat.appendPropId)
                        # Format stat value
                        stat_value = stat.statValue
                        if isinstance(stat_value, float) and stat_value < 100:
                            stat_display = f"{stat_value:.1f}%"
                        else:
                            stat_display = f"{stat_value:.0f}"
                        print(f"      {stat_name}: {stat_display}")


async def main():
    """Main function."""
    uid = 657846809
    
    print(f"Fetching player information for UID: {uid}")
    print("=" * 70)
    
    data = await fetch_player_data(uid)
    
    if data:
        display_player_info(data)
        display_character_info(data)
        print("\n" + "=" * 70)
        print("[SUCCESS] Data fetched and parsed successfully!")
        print(f"Response TTL: {data.ttl} seconds")
    else:
        print("\n[ERROR] Failed to fetch or parse player data")


if __name__ == "__main__":
    asyncio.run(main())

