"""
Fetch raw API response from Enka Network API and create Pydantic models.
"""

import asyncio
import json
import aiohttp
from typing import Optional, List, Dict, Any, Union


async def fetch_raw_api_response(uid: int):
    """
    Fetch raw JSON response from Enka Network API.
    
    Args:
        uid: Genshin Impact player UID
    """
    url = f"https://enka.network/api/uid/{uid}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"API returned status {response.status}")
                text = await response.text()
                print(f"Response: {text}")
                return None


async def main():
    """Fetch and display raw API response."""
    uid = 657846809
    
    print(f"Fetching raw API response for UID: {uid}")
    print("=" * 70)
    
    data = await fetch_raw_api_response(uid)
    
    if data:
        # Save to file for inspection (save in tests directory)
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "raw_api_response.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Raw API response saved to '{json_path}'")
        print("\nResponse structure:")
        print(f"  Top-level keys: {list(data.keys())}")
        
        # Inspect playerInfo structure
        if "playerInfo" in data:
            player_info = data["playerInfo"]
            print(f"\n  playerInfo keys: {list(player_info.keys())}")
            if "showAvatarInfoList" in player_info:
                print(f"    showAvatarInfoList length: {len(player_info['showAvatarInfoList'])}")
                if len(player_info["showAvatarInfoList"]) > 0:
                    first_avatar = player_info["showAvatarInfoList"][0]
                    print(f"    First avatar keys: {list(first_avatar.keys())}")
                    if "avatarId" in first_avatar:
                        print(f"    avatarId type: {type(first_avatar['avatarId']).__name__}, value: {first_avatar['avatarId']}")
        
        # Inspect avatarInfoList structure
        if "avatarInfoList" in data:
            print(f"\n  avatarInfoList length: {len(data['avatarInfoList'])}")
            if len(data["avatarInfoList"]) > 0:
                first_char = data["avatarInfoList"][0]
                print(f"    First character keys: {list(first_char.keys())}")
                if "equipList" in first_char:
                    print(f"      equipList length: {len(first_char['equipList'])}")
                    if len(first_char["equipList"]) > 0:
                        first_equip = first_char["equipList"][0]
                        print(f"        First equipment keys: {list(first_equip.keys())}")
                        if "propValue" in first_equip:
                            print(f"        propValue type: {type(first_equip['propValue']).__name__}, value: {first_equip['propValue']}")
    else:
        print("Failed to fetch API response")


if __name__ == "__main__":
    asyncio.run(main())

