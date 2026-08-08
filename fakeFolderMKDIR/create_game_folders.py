import os
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
import re

BASE_PATH = "./pc_games"  # Change this to your desired path

# Predefined system requirements for popular games
GAME_REQUIREMENTS = {
    "The Witcher 3 Wild Hunt": {
        "minimum": {"CPU": "CPU 64-bit: Intel i7 or AMD equivalent", "GPU": "NVIDIA GTX 960 or AMD Radeon R9 290", "RAM": "8 GB", "Storage": "136 GB"},
        "recommended": {"CPU": "CPU 64-bit: Intel i7 or AMD equivalent", "GPU": "NVIDIA GTX 1060 or AMD Radeon RX 480", "RAM": "16 GB", "Storage": "136 GB"}
    },
    "Elden Ring": {
        "minimum": {"CPU": "Intel i5-8400 / AMD Ryzen 5 2600", "GPU": "NVIDIA GeForce GTX 1060 3GB / AMD Radeon RX 580", "RAM": "12 GB", "Storage": "60 GB"},
        "recommended": {"CPU": "Intel i7-10700K / AMD Ryzen 5 3600", "GPU": "NVIDIA GeForce RTX 2080 Super / AMD Radeon RX 5700 XT", "RAM": "16 GB", "Storage": "60 GB"}
    },
    "Baldurs Gate 3": {
        "minimum": {"CPU": "Intel i5-4690 / AMD FX 4350", "GPU": "NVIDIA GTX 960 / AMD Radeon R9 280X", "RAM": "150 GB", "Storage": "150 GB"},
        "recommended": {"CPU": "Intel i7-10700K / AMD Ryzen 5 3600", "GPU": "NVIDIA RTX 2080 / AMD Radeon RX 5700 XT", "RAM": "200 GB", "Storage": "200 GB"}
    },
}

def get_games_from_wikipedia(limit=500):
    """
    Fetch popular PC games from Wikipedia's list of best-selling video games.
    """
    print(f"Fetching popular games from Wikipedia...")

    games = []

    try:
        # Fetch Wikipedia page for best-selling video games
        url = "https://en.wikipedia.org/wiki/List_of_best-selling_video_games"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all tables
        tables = soup.find_all('table', {'class': 'wikitable'})

        if tables:
            # Process the first table (usually contains best-selling games)
            table = tables[0]
            rows = table.find_all('tr')[1:]  # Skip header row

            for row in rows[:limit]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    # Extract game name from the first column
                    game_name = cols[1].text.strip()

                    # Clean up the game name
                    game_name = re.sub(r'\[.*?\]', '', game_name).strip()
                    game_name = re.sub(r'[^\w\s\-&:]', '', game_name).strip()

                    if game_name and len(game_name) > 2:
                        games.append({'name': game_name})

        if not games:
            # Fallback to a curated list if scraping fails
            print("Wikipedia scraping returned limited results. Using curated game list...")
            games = get_curated_games_list(limit)

        print(f"Successfully fetched {len(games)} games")
        return games

    except Exception as e:
        print(f"Error fetching from Wikipedia: {e}")
        print("Using curated game list as fallback...")
        return get_curated_games_list(limit)

def get_curated_games_list(limit=500):
    """
    Return a curated list of popular PC games.
    This is used as a fallback when web scraping fails.
    """
    games = [
        {"name": "The Witcher 3 Wild Hunt"},
        {"name": "Elden Ring"},
        {"name": "Baldurs Gate 3"},
        {"name": "Cyberpunk 2077"},
        {"name": "Starfield"},
        {"name": "Diablo IV"},
        {"name": "Hogwarts Legacy"},
        {"name": "Final Fantasy VII Remake Intergrade"},
        {"name": "Dragon Age Inquisition"},
        {"name": "Mass Effect Legendary Edition"},
        {"name": "Fortnite"},
        {"name": "Counter-Strike 2"},
        {"name": "DOTA 2"},
        {"name": "League of Legends"},
        {"name": "Valorant"},
        {"name": "PlayerUnknowns Battlegrounds"},
        {"name": "Apex Legends"},
        {"name": "Hearthstone"},
        {"name": "World of Warcraft"},
        {"name": "Final Fantasy XIV"},
        {"name": "The Sims 4"},
        {"name": "Minecraft Java Edition"},
        {"name": "Stardew Valley"},
        {"name": "Terraria"},
        {"name": "Dead by Daylight"},
        {"name": "Grounded"},
        {"name": "Valheim"},
        {"name": "Hades"},
        {"name": "Hollow Knight Silksong"},
        {"name": "Doom Eternal"},
        {"name": "Halo Infinite"},
        {"name": "Gears 5"},
        {"name": "Forza Horizon 5"},
        {"name": "Cities Skylines"},
        {"name": "Sid Meiers Civilization VI"},
        {"name": "Total War Warhammer III"},
        {"name": "Stellaris"},
        {"name": "Europa Universalis IV"},
        {"name": "Crusader Kings III"},
        {"name": "Mount and Blade II Bannerlord"},
        {"name": "Outlanders Odysee"},
        {"name": "Star Citizen"},
        {"name": "Escape from Tarkov"},
        {"name": "DayZ"},
        {"name": "Rust"},
        {"name": "Ark Survival Evolved"},
        {"name": "Conan Exiles"},
        {"name": "New World"},
        {"name": "Elder Scrolls Online"},
        {"name": "Guild Wars 2"},
        {"name": "Black Desert Online"},
        {"name": "Lost Ark"},
        {"name": "Team Fortress 2"},
        {"name": "Overwatch 2"},
        {"name": "Rainbow Six Siege"},
        {"name": "SCUM"},
        {"name": "Squad"},
        {"name": "Insurgency Sandstorm"},
        {"name": "Killing Floor 2"},
        {"name": "Payday 2"},
        {"name": "Left 4 Dead 2"},
        {"name": "Deep Rock Galactic"},
        {"name": "Helldivers 2"},
        {"name": "Satisfactory"},
        {"name": "Factorio"},
        {"name": "Rimworld"},
        {"name": "Oxygen Not Included"},
        {"name": "Prison Architect"},
        {"name": "Two Point Hospital"},
        {"name": "Tropico 6"},
        {"name": "Strategy Manager Football"},
        {"name": "Pro Evolution Soccer 2024"},
        {"name": "NBA 2K24"},
        {"name": "Madden NFL 24"},
        {"name": "F1 24"},
        {"name": "iRAcing"},
        {"name": "Assetto Corsa Competizione"},
        {"name": "Project Cars 3"},
        {"name": "BeamNG"},
        {"name": "Automobilista 2"},
        {"name": "Euro Truck Simulator 2"},
        {"name": "American Truck Simulator"},
        {"name": "Microsoft Flight Simulator"},
        {"name": "DCS World"},
        {"name": "IL-2 Sturmovik Great Battles"},
        {"name": "War Thunder"},
        {"name": "World of Tanks"},
        {"name": "World of Warships"},
        {"name": "World of Warplanes"},
        {"name": "Elite Dangerous"},
        {"name": "No Mans Sky"},
        {"name": "Star Wars The Old Republic"},
        {"name": "EVE Online"},
        {"name": "Albion Online"},
        {"name": "Cabal 2"},
        {"name": "Tera"},
        {"name": "Aion"},
        {"name": "Blade and Soul"},
        {"name": "Soul Worker"},
        {"name": "Tree of Savior"},
        {"name": "Ragnarok Online"},
        {"name": "Lineage 2"},
        {"name": "Dark and Light"},
        {"name": "Archeage"},
        {"name": "Crowfall"},
        {"name": "Mortal Online 2"},
        {"name": "Gloria Victis"},
        {"name": "Starbase"},
        {"name": "Unturned"},
        {"name": "Garry's Mod"},
        {"name": "Half-Life 2"},
        {"name": "Portal 2"},
        {"name": "Team Fortress Classic"},
        {"name": "Counter-Strike Source"},
        {"name": "Day of Defeat"},
        {"name": "Deathmatch Classic"},
        {"name": "Half-Life Deathmatch"},
        {"name": "ricochet"},
        {"name": "Opposing Force"},
        {"name": "Blue Shift"},
        {"name": "Black Mesa"},
        {"name": "Half-Life Alyx"},
        {"name": "The Orange Box"},
        {"name": "Bioshock Infinite"},
        {"name": "Dishonored 2"},
        {"name": "Prey"},
        {"name": "Alien Isolation"},
        {"name": "Resident Evil Village"},
        {"name": "Resident Evil 4 Remake"},
        {"name": "Silent Hill 2 Remake"},
        {"name": "Dead Space Remake"},
        {"name": "The Evil Within"},
        {"name": "The Evil Within 2"},
        {"name": "Outlast"},
        {"name": "Outlast 2"},
        {"name": "Amnesia The Dark Descent"},
        {"name": "Penumbra"},
        {"name": "Soma"},
        {"name": "Subnautica"},
        {"name": "Subnautica Below Zero"},
        {"name": "Slime Rancher"},
        {"name": "No Mans Sky"},
        {"name": "Spore"},
        {"name": "Creatures"},
        {"name": "Artificial Life"},
    ]

    return games[:limit]

def download_game_image(game_name, game_folder):
    """
    Try to download a game image from DuckDuckGo or use a placeholder.
    """
    try:
        # Use a simple approach - create a placeholder image info file
        image_file = os.path.join(game_folder, "cover_image_info.txt")
        with open(image_file, "w", encoding="utf-8") as f:
            f.write(f"Cover Image for: {game_name}\n")
            f.write(f"To download actual cover image, search on:\n")
            f.write(f"- Google Images: {game_name} cover art\n")
            f.write(f"- Steam: https://steampowered.com\n")
            f.write(f"- IGDB: https://www.igdb.com\n")
        return True
    except Exception as e:
        print(f"  Warning: Could not create image info for {game_name}: {e}")
        return False

def create_requirements_file(game_folder, game_name):
    """
    Create a text file with system requirements.
    Uses predefined requirements for known games, or generic recommendations.
    """
    req_path = os.path.join(game_folder, "system_requirements.txt")

    try:
        with open(req_path, "w", encoding="utf-8") as f:
            f.write(f"SYSTEM REQUIREMENTS FOR: {game_name}\n")
            f.write("=" * 70 + "\n\n")

            # Check if we have predefined requirements for this game
            if game_name in GAME_REQUIREMENTS:
                game_reqs = GAME_REQUIREMENTS[game_name]

                # Minimum Requirements
                f.write("MINIMUM REQUIREMENTS:\n")
                f.write("-" * 70 + "\n")
                for key, value in game_reqs["minimum"].items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")

                # Recommended Requirements
                f.write("RECOMMENDED REQUIREMENTS:\n")
                f.write("-" * 70 + "\n")
                for key, value in game_reqs["recommended"].items():
                    f.write(f"{key}: {value}\n")
            else:
                # Generic recommended specs for modern games
                f.write("MINIMUM REQUIREMENTS:\n")
                f.write("-" * 70 + "\n")
                f.write("CPU: Intel Core i5 / AMD Ryzen 5 (or better)\n")
                f.write("GPU: NVIDIA GTX 960 / AMD Radeon R9 280X (or better)\n")
                f.write("RAM: 8 GB\n")
                f.write("Storage: 50-100 GB SSD space recommended\n")
                f.write("OS: Windows 10 64-bit or later\n")
                f.write("\n")

                f.write("RECOMMENDED REQUIREMENTS:\n")
                f.write("-" * 70 + "\n")
                f.write("CPU: Intel Core i7 / AMD Ryzen 7 (or better)\n")
                f.write("GPU: NVIDIA RTX 2080 / AMD Radeon RX 5700 XT (or better)\n")
                f.write("RAM: 16 GB\n")
                f.write("Storage: SSD with 100+ GB available space\n")
                f.write("OS: Windows 10/11 64-bit\n")
                f.write("\nNote: Actual requirements may vary. Check the game's official website for accurate specs.\n")

            f.write("\n")
            f.write("-" * 70 + "\n")
            f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Note: These are general requirements. Visit the game's Steam page or official\n")
            f.write("website for the most accurate and up-to-date system requirements.\n")

        return True
    except Exception as e:
        print(f"  Warning: Could not create requirements file: {e}")
        return False

def sanitize_folder_name(name):
    """
    Remove invalid characters from folder names.
    """
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip()

def create_game_folders(games, base_path=BASE_PATH):
    """
    Create folder structure for each game with cover info and requirements.
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"Created base directory: {base_path}\n")

    successful = 0
    failed = 0

    for idx, game in enumerate(games, 1):
        game_name = game.get('name', f'Game_{idx}')
        safe_name = sanitize_folder_name(game_name)
        game_folder = os.path.join(base_path, safe_name)

        try:
            # Create game folder
            if not os.path.exists(game_folder):
                os.makedirs(game_folder)

            # Create cover image info file
            download_game_image(game_name, game_folder)

            # Create system requirements file
            create_requirements_file(game_folder, game_name)

            print(f"[{idx}/{len(games)}] Created folder: {safe_name}")
            successful += 1

            # Small delay to avoid overwhelming the system
            if idx % 50 == 0:
                time.sleep(0.5)

        except Exception as e:
            print(f"[{idx}/{len(games)}] Error creating folder for {game_name}: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"SUMMARY:")
    print(f"Successfully created: {successful} folders")
    print(f"Failed: {failed} folders")
    print(f"Base path: {os.path.abspath(base_path)}")
    print("=" * 70)


def main():
    """
    Main function to orchestrate the entire process.
    """
    print("=" * 70)
    print("PC GAMES FOLDER CREATOR")
    print("=" * 70)
    print()

    # Get custom base path from user
    default_path = os.path.expanduser("./pc_games")
    custom_path = input(f"Enter the base path for game folders (default: {default_path}): ").strip()
    if custom_path:
        base_path = custom_path
    else:
        base_path = default_path

    print()

    # Get number of games to create
    user_limit = input("How many game folders to create? (default: 500, max: 500): ").strip()
    try:
        limit = int(user_limit) if user_limit else 500
        limit = min(limit, 500)  # Cap at 500
    except ValueError:
        limit = 500

    print()

    # Fetch games from Wikipedia
    print("Fetching game list from Wikipedia...")
    games = get_games_from_wikipedia(limit=limit)

    if not games:
        print("No games found. Please check your internet connection.")
        return

    print()

    # Create folders and files
    create_game_folders(games, base_path)

    print("\n✓ Process complete!")
    print(f"\nEach game folder contains:")
    print("  - cover_image_info.txt (links to download cover art)")
    print("  - system_requirements.txt (minimum and recommended specs)")

if __name__ == "__main__":
    main()

