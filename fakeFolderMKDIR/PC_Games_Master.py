import os
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

BASE_PATH = "./pc_games"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Predefined system requirements for popular games
GAME_REQUIREMENTS = {
    "The Witcher 3 Wild Hunt": {
        "minimum": {"CPU": "CPU 64-bit: Intel i7 or AMD equivalent", "GPU": "NVIDIA GTX 960 or AMD Radeon R9 290", "RAM": "8 GB", "Storage": "136 GB"},
        "recommended": {"CPU": "CPU 64-bit: Intel i7 or AMD equivalent", "GPU": "NVIDIA GTX 1060 or AMD Radeon RX 480", "RAM": "16 GB", "Storage": "136 GB"}
    },
}

def get_curated_games_list(limit=500):
    """Return a curated list of popular PC games."""
    games = [
        {"name": "The Witcher 3 Wild Hunt"},
        {"name": "Elden Ring"},
    ]

    return games[:limit]

def sanitize_folder_name(name):
    """Remove invalid characters from folder names."""
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip()

def create_game_folders_step(games, base_path=BASE_PATH):
    """Step 1: Create game folders."""
    print("\n" + "=" * 70)
    print("STEP 1: CREATING GAME FOLDERS")
    print("=" * 70)

    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"✓ Created base directory: {base_path}\n")
    else:
        print(f"✓ Base directory already exists: {base_path}\n")

    game_folders = [f for f in os.listdir(base_path) 
                   if os.path.isdir(os.path.join(base_path, f))]

    if game_folders:
        print(f"✓ Found {len(game_folders)} existing folders")
        return

    successful = 0
    failed = 0

    for idx, game in enumerate(games, 1):
        game_name = game.get('name', f'Game_{idx}')
        safe_name = sanitize_folder_name(game_name)
        game_folder = os.path.join(base_path, safe_name)

        try:
            if not os.path.exists(game_folder):
                os.makedirs(game_folder)

            # Create placeholder requirements file
            req_file = os.path.join(game_folder, "system_requirements.txt")
            if not os.path.exists(req_file):
                content = f"SYSTEM REQUIREMENTS FOR: {game_name}\n"
                content += "=" * 70 + "\n\n"
                content += "MINIMUM REQUIREMENTS:\n"
                content += "-" * 70 + "\n"
                content += "Loading...\n\n"
                content += "RECOMMENDED REQUIREMENTS:\n"
                content += "-" * 70 + "\n"
                content += "Loading...\n"

                with open(req_file, 'w', encoding='utf-8') as f:
                    f.write(content)

            print(f"[{idx}/{len(games)}] ✓ {safe_name}")
            successful += 1

        except Exception as e:
            print(f"[{idx}/{len(games)}] ✗ Error: {safe_name}")
            failed += 1

    print(f"\n✓ Created: {successful} folders")
    print(f"✗ Failed: {failed} folders")

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

def fetch_requirements_step(base_path=BASE_PATH):
    """Step 2: Fetch real system requirements from Steam."""
    print("\n" + "=" * 70)
    print("STEP 2: FETCHING REAL SYSTEM REQUIREMENTS FROM STEAM")
    print("=" * 70 + "\n")

    if not os.path.exists(base_path):
        print("✗ Base path does not exist")
        return

    game_folders = sorted([f for f in os.listdir(base_path) 
                          if os.path.isdir(os.path.join(base_path, f))])

    print(f"Found {len(game_folders)} game folders\n")

    successful = 0
    not_found = 0
    skipped = 0

    for idx, game_folder in enumerate(game_folders, 1):
        game_name = game_folder
        game_path = os.path.join(base_path, game_folder)
        req_file = os.path.join(game_path, "system_requirements.txt")

        # Check if already has real data
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

            content = format_requirements_file(game_name, requirements)
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write(content)

            time.sleep(0.3)

        except Exception:
            print("✗ Error")

    print(f"\n✓ Already updated: {skipped} games")
    print(f"✓ Successfully fetched: {successful} games")
    print(f"✗ Not found on Steam: {not_found} games")

def fetch_steam_app_id(game_name):
    """Get Steam app ID for a game."""
    try:
        search_url = f"https://steamcommunity.com/actions/SearchApps/{quote(game_name)}"
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        apps = response.json()
        if apps:
            return apps[0]['appid']
        return None
    except Exception:
        return None

def fetch_steam_cover_image(app_id, game_name, game_folder):
    """Download cover image from Steam."""
    try:
        cover_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/library_600x900_2x.jpg"
        response = requests.get(cover_url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            cover_path = os.path.join(game_folder, "cover.jpg")
            with open(cover_path, 'wb') as f:
                f.write(response.content)
            return True

        # Try alternative URL
        cover_url_alt = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
        response = requests.get(cover_url_alt, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            cover_path = os.path.join(game_folder, "cover.jpg")
            with open(cover_path, 'wb') as f:
                f.write(response.content)
            return True

        return False
    except Exception:
        return False

def download_covers_step(base_path=BASE_PATH):
    """Step 3: Download actual cover images."""
    print("\n" + "=" * 70)
    print("STEP 3: DOWNLOADING ACTUAL COVER IMAGES FROM STEAM")
    print("=" * 70 + "\n")

    if not os.path.exists(base_path):
        print("✗ Base path does not exist")
        return

    game_folders = sorted([f for f in os.listdir(base_path) 
                          if os.path.isdir(os.path.join(base_path, f))])

    print(f"Found {len(game_folders)} game folders\n")

    downloaded = 0
    already_exists = 0
    failed = 0

    for idx, game_folder in enumerate(game_folders, 1):
        game_name = game_folder
        game_path = os.path.join(base_path, game_folder)
        cover_path = os.path.join(game_path, "cover.jpg")

        if os.path.exists(cover_path):
            already_exists += 1
            continue

        try:
            print(f"[{idx}/{len(game_folders)}] {game_name}...", end=" ", flush=True)

            app_id = fetch_steam_app_id(game_name)
            if app_id:
                if fetch_steam_cover_image(app_id, game_name, game_path):
                    print("✓ Steam")
                    downloaded += 1
                    time.sleep(0.2)
                    continue

            print("✗ Failed")
            failed += 1

        except Exception:
            print("✗ Error")
            failed += 1

    print(f"\n✓ Already exists: {already_exists} images")
    print(f"✓ Downloaded: {downloaded} images")
    print(f"✗ Failed: {failed} images")

def cleanup_step(base_path=BASE_PATH):
    """Step 4: Clean up old placeholder files."""
    print("\n" + "=" * 70)
    print("STEP 4: CLEANING UP OLD FILES")
    print("=" * 70 + "\n")

    if not os.path.exists(base_path):
        print("✗ Base path does not exist")
        return

    game_folders = [f for f in os.listdir(base_path) 
                   if os.path.isdir(os.path.join(base_path, f))]

    print(f"Found {len(game_folders)} game folders\n")

    removed = 0

    for idx, game_folder in enumerate(game_folders, 1):
        game_path = os.path.join(base_path, game_folder)
        info_file = os.path.join(game_path, "cover_image_info.txt")

        if os.path.exists(info_file):
            try:
                os.remove(info_file)
                print(f"[{idx}/{len(game_folders)}] {game_folder}... ✓")
                removed += 1
            except Exception:
                pass

    print(f"\n✓ Removed: {removed} old info files")

def select_directory(start_path="."):
    """Text-based menu to navigate and select a directory."""
    current_path = os.path.abspath(start_path)

    while True:
        print("\n" + "=" * 70)
        print(f"CURRENT DIRECTORY: {current_path}")
        print("=" * 70)

        try:
            # Get list of directories
            items = os.listdir(current_path)
            directories = [d for d in items if os.path.isdir(os.path.join(current_path, d))]
            directories.sort()

            # Print options
            print("0: [Select this directory]")
            print("1: [Go up to parent directory (..)]")

            for i, d in enumerate(directories, 2):
                print(f"{i}: {d}")

            print("\nEnter number to navigate, or 'c' to cancel and use default:")
            choice = input("> ").strip().lower()

            if choice == 'c':
                return None

            if choice == '0':
                return current_path

            if choice == '1':
                current_path = os.path.abspath(os.path.join(current_path, os.pardir))
                continue

            # Try to navigate to chosen directory
            try:
                idx = int(choice)
                if 2 <= idx < len(directories) + 2:
                    selected_dir = directories[idx - 2]
                    current_path = os.path.join(current_path, selected_dir)
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        except PermissionError:
            print(f"Permission denied to access {current_path}.")
            current_path = os.path.abspath(os.path.join(current_path, os.pardir))
            time.sleep(1)

def main():
    """Main function - Menu workflow."""
    print("=" * 70)
    print("PC GAMES DATABASE BUILDER")
    print("=" * 70)
    print()

    print("Please select the base directory for game folders:")
    selected_path = select_directory()

    if selected_path:
        base_path = selected_path
    else:
        base_path = BASE_PATH

    print(f"\nUsing base path: {base_path}")

    while True:
        print("\n" + "=" * 70)
        print("MAIN MENU")
        print("=" * 70)
        print("1. Create game folders")
        print("2. Download system requirements")
        print("3. Download cover images")
        print("4. Clean up old placeholder files")
        print("5. Exit")
        print()

        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            user_limit = input("\nHow many games to create? (default: 500, max: 500): ").strip()
            try:
                limit = int(user_limit) if user_limit else 500
                limit = min(limit, 500)
            except ValueError:
                limit = 500

            games = get_curated_games_list(limit)
            create_game_folders_step(games, base_path)

        elif choice == '2':
            fetch_requirements_step(base_path)

        elif choice == '3':
            download_covers_step(base_path)

        elif choice == '4':
            cleanup_step(base_path)

        elif choice == '5':
            print("\nExiting program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
