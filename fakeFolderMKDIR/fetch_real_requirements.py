import os
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import quote
from datetime import datetime

BASE_GAMES_PATH = "./pc_games"

# Headers for web requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def parse_steam_requirements(html_text):
    """
    Parse Steam requirements HTML and extract CPU, GPU, RAM, Storage.
    Returns dict with formatted specs.
    """
    if not html_text:
        return {}

    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', html_text)
    text = re.sub(r'\n+', '\n', text).strip()

    specs = {}
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract CPU
        if re.search(r'cpu|processor', line, re.I):
            specs['CPU'] = line
        # Extract GPU
        elif re.search(r'gpu|graphics|video|directx', line, re.I):
            specs['GPU'] = line
        # Extract RAM/Memory
        elif re.search(r'memory|ram|gb', line, re.I):
            specs['RAM'] = line
        # Extract Storage
        elif re.search(r'storage|disk|space', line, re.I):
            specs['Storage'] = line

    return specs


def fetch_steam_requirements(game_name):
    """
    Fetch game requirements from Steam store.
    Returns dict with 'minimum' and/or 'recommended' specs.
    """
    try:
        # Search for the game on Steam
        search_url = f"https://steamcommunity.com/actions/SearchApps/{quote(game_name)}"
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        apps = response.json()
        if not apps:
            return None

        # Get the first result
        app_id = apps[0]['appid']

        # Fetch the app details
        app_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        response = requests.get(app_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        app_data = response.json()
        if not app_data.get(str(app_id), {}).get('success'):
            return None

        data = app_data[str(app_id)]['data']

        # Extract requirements
        requirements = {}

        if 'pc_requirements' in data:
            pc_reqs = data['pc_requirements']

            if 'minimum' in pc_reqs and pc_reqs['minimum']:
                min_specs = parse_steam_requirements(pc_reqs['minimum'])
                if min_specs:
                    requirements['minimum'] = min_specs

            if 'recommended' in pc_reqs and pc_reqs['recommended']:
                rec_specs = parse_steam_requirements(pc_reqs['recommended'])
                if rec_specs:
                    requirements['recommended'] = rec_specs

        return requirements if requirements else None

    except Exception as e:
        return None


def format_requirements_file(game_name, requirements):
    """
    Format requirements into EXACT SAME format as before.
    """
    content = f"SYSTEM REQUIREMENTS FOR: {game_name}\n"
    content += "=" * 70 + "\n\n"

    if requirements is None:
        content += "MINIMUM REQUIREMENTS:\n"
        content += "-" * 70 + "\n"
        content += "System requirements not available.\n\n"
        content += "RECOMMENDED REQUIREMENTS:\n"
        content += "-" * 70 + "\n"
        content += "System requirements not available.\n"
    else:
        # Minimum Requirements
        content += "MINIMUM REQUIREMENTS:\n"
        content += "-" * 70 + "\n"

        if 'minimum' in requirements:
            min_specs = requirements['minimum']
            if 'CPU' in min_specs:
                content += f"CPU: {min_specs['CPU']}\n"
            if 'GPU' in min_specs:
                content += f"GPU: {min_specs['GPU']}\n"
            if 'RAM' in min_specs:
                content += f"RAM: {min_specs['RAM']}\n"
            if 'Storage' in min_specs:
                content += f"Storage: {min_specs['Storage']}\n"
            if not min_specs:
                content += "System requirements not available.\n"
        else:
            content += "System requirements not available.\n"

        content += "\n"

        # Recommended Requirements
        content += "RECOMMENDED REQUIREMENTS:\n"
        content += "-" * 70 + "\n"

        if 'recommended' in requirements:
            rec_specs = requirements['recommended']
            if 'CPU' in rec_specs:
                content += f"CPU: {rec_specs['CPU']}\n"
            if 'GPU' in rec_specs:
                content += f"GPU: {rec_specs['GPU']}\n"
            if 'RAM' in rec_specs:
                content += f"RAM: {rec_specs['RAM']}\n"
            if 'Storage' in rec_specs:
                content += f"Storage: {rec_specs['Storage']}\n"
            if not rec_specs:
                content += "System requirements not available.\n"
        else:
            content += "System requirements not available.\n"

    content += "\n"
    content += "-" * 70 + "\n"
    content += f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += "Source: Fetched from Steam Web API\n"

    return content


def update_game_folders(base_path=BASE_GAMES_PATH, max_games=None):
    """
    Update all game folders with real requirements from Steam.
    """
    if not os.path.exists(base_path):
        print(f"Error: Base path does not exist: {base_path}")
        return

    game_folders = sorted([f for f in os.listdir(base_path) 
                          if os.path.isdir(os.path.join(base_path, f))])

    if max_games:
        game_folders = game_folders[:max_games]

    print(f"\nFound {len(game_folders)} game folders")
    print("=" * 70)
    print()

    successful = 0
    not_found = 0
    failed = 0

    for idx, game_folder in enumerate(game_folders, 1):
        game_name = game_folder
        game_path = os.path.join(base_path, game_folder)

        try:
            # Fetch requirements from Steam
            print(f"[{idx}/{len(game_folders)}] {game_name}...", end=" ", flush=True)
            requirements = fetch_steam_requirements(game_name)

            if requirements:
                print("✓ Found")
                successful += 1
            else:
                print("✗ Not found")
                not_found += 1

            # Write to file with exact format
            req_file = os.path.join(game_path, "system_requirements.txt")
            content = format_requirements_file(game_name, requirements)

            with open(req_file, 'w', encoding='utf-8') as f:
                f.write(content)

            # Rate limiting - be nice to Steam servers
            time.sleep(0.3)

        except Exception as e:
            print(f"✗ Error")
            failed += 1

    print("\n" + "=" * 70)
    print("SUMMARY:")
    print(f"Successfully fetched: {successful} games")
    print(f"Not found on Steam: {not_found} games")
    print(f"Failed: {failed} games")
    print("=" * 70)


def main():
    """
    Main function.
    """
    print("=" * 70)
    print("FETCH REAL GAME REQUIREMENTS FROM STEAM")
    print("=" * 70)
    print()

    # Get custom path
    custom_path = input(f"Enter path to game folders (default: {BASE_GAMES_PATH}): ").strip()
    if custom_path:
        base_path = custom_path
    else:
        base_path = BASE_GAMES_PATH

    print()

    # Ask how many games to update
    max_input = input("How many games to update? (default: all): ").strip()
    max_games = None
    if max_input and max_input.isdigit():
        max_games = int(max_input)

    print()

    # Confirm before proceeding
    confirm = input("This will fetch real specs from Steam and update all files. Continue? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Cancelled.")
        return

    print()

    update_game_folders(base_path, max_games)

    print("\n✓ Process complete!")
    print("\nFile format maintained identical to original.")
    print("Text files updated with real data from Steam API.")


if __name__ == "__main__":
    main()

