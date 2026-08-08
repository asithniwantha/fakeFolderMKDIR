import os
import requests
from datetime import datetime
import re
import time
from urllib.parse import quote

BASE_GAMES_PATH = "./pc_games"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def parse_steam_requirements(html_text):
    """Parse Steam requirements HTML and extract specs."""
    if not html_text:
        return {}

    text = re.sub('<[^<]+?>', '', html_text)
    text = re.sub(r'\n+', '\n', text).strip()
    specs = {}
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.search(r'cpu|processor', line, re.I):
            specs['CPU'] = line
        elif re.search(r'gpu|graphics|video|directx', line, re.I):
            specs['GPU'] = line
        elif re.search(r'memory|ram|gb', line, re.I):
            specs['RAM'] = line
        elif re.search(r'storage|disk|space', line, re.I):
            specs['Storage'] = line

    return specs


def fetch_steam_requirements(game_name):
    """Fetch game requirements from Steam store."""
    try:
        search_url = f"https://steamcommunity.com/actions/SearchApps/{quote(game_name)}"
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        apps = response.json()
        if not apps:
            return None

        app_id = apps[0]['appid']
        app_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        response = requests.get(app_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        app_data = response.json()
        if not app_data.get(str(app_id), {}).get('success'):
            return None

        data = app_data[str(app_id)]['data']
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

    except Exception:
        return None


def format_requirements_file(game_name, requirements):
    """Format requirements into text file."""
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


def main():
    """Main function - update remaining games."""
    print("=" * 70)
    print("RESUME: FETCH REMAINING GAME REQUIREMENTS FROM STEAM")
    print("=" * 70)
    print()

    base_path = "./pc_games"

    if not os.path.exists(base_path):
        print(f"Error: Base path does not exist: {base_path}")
        return

    game_folders = sorted([f for f in os.listdir(base_path) 
                          if os.path.isdir(os.path.join(base_path, f))])

    print(f"Found {len(game_folders)} game folders\n")

    successful = 0
    skipped = 0  # Already have Steam data
    not_found = 0
    failed = 0

    for idx, game_folder in enumerate(game_folders, 1):
        game_name = game_folder
        game_path = os.path.join(base_path, game_folder)
        req_file = os.path.join(game_path, "system_requirements.txt")

        # Check if file already has Steam data
        if os.path.exists(req_file):
            with open(req_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Steam Web API' in content:
                    skipped += 1
                    continue

        try:
            print(f"[{idx}/{len(game_folders)}] {game_name}...", end=" ", flush=True)
            requirements = fetch_steam_requirements(game_name)

            if requirements:
                print("✓ Found")
                successful += 1
            else:
                print("✗ Not found")
                not_found += 1

            # Write to file
            content = format_requirements_file(game_name, requirements)

            with open(req_file, 'w', encoding='utf-8') as f:
                f.write(content)

            # Rate limiting
            time.sleep(0.3)

        except Exception:
            print(f"✗ Error")
            failed += 1

    print("\n" + "=" * 70)
    print("SUMMARY:")
    print(f"Already updated (skipped): {skipped} games")
    print(f"Successfully fetched: {successful} games")
    print(f"Not found on Steam: {not_found} games")
    print(f"Failed: {failed} games")
    print("=" * 70)


if __name__ == "__main__":
    main()
