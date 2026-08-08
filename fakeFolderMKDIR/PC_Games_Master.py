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
        {"name": "The Outer Worlds"},
        {"name": "Persona 4 Golden"},
        {"name": "Persona 5 Royal"},
        {"name": "Fire Emblem Three Houses"},
        {"name": "XCOM 2"},
        {"name": "Civilization V"},
        {"name": "Civilization IV"},
        {"name": "Tropico 5"},
        {"name": "SimCity"},
        {"name": "Cities Skylines II"},
        {"name": "Greedfall"},
        {"name": "Elex 2"},
        {"name": "Kingdom Come Deliverance"},
        {"name": "Mount and Blade"},
        {"name": "Divinity Original Sin 2"},
        {"name": "Pillars of Eternity II Deadfire"},
        {"name": "Wasteland 2"},
        {"name": "Wasteland 3"},
        {"name": "Fallout New Vegas"},
        {"name": "Fallout 4"},
        {"name": "Skyrim"},
        {"name": "Oblivion"},
        {"name": "Morrowind"},
        {"name": "Daggerfall"},
        {"name": "The Outer Wilds"},
        {"name": "Portal Companion Collection"},
        {"name": "Antichamber"},
        {"name": "The Talos Principle"},
        {"name": "Q.U.B.E. 2"},
        {"name": "Stephen's Sausage Roll"},
        {"name": "Witness"},
        {"name": "Braid"},
        {"name": "Fran Bow"},
        {"name": "Firewatch"},
        {"name": "What Remains of Edith Finch"},
        {"name": "Oxenfree"},
        {"name": "Thimbleweed Park"},
        {"name": "Grim Fandango"},
        {"name": "Monkey Island"},
        {"name": "Return to Monkey Island"},
        {"name": "Day of the Tentacle"},
        {"name": "Maniac Mansion"},
        {"name": "Full Throttle"},
        {"name": "Broken Age"},
        {"name": "Telltale Games"},
        {"name": "Life is Strange"},
        {"name": "Max Caulfield Adventure"},
        {"name": "Before the Storm"},
        {"name": "True Colors"},
        {"name": "The Walking Dead"},
        {"name": "The Wolf Among Us"},
        {"name": "Tales from the Borderlands"},
        {"name": "Game of Thrones Telltale"},
        {"name": "Batman The Telltale Series"},
        {"name": "Back to the Future Game"},
        {"name": "Jurassic Park The Game"},
        {"name": "Law and Order Legacies"},
        {"name": "Minecraft"},
        {"name": "Minecraft Dungeons"},
        {"name": "Minecraft Legends"},
        {"name": "The Legend of Zelda Breath of Wild"},
        {"name": "The Legend of Zelda Tears of Kingdom"},
        {"name": "Ocarina of Time"},
        {"name": "Majoras Mask"},
        {"name": "Windwaker"},
        {"name": "Twilight Princess"},
        {"name": "Skyward Sword"},
        {"name": "Link Between Worlds"},
        {"name": "Links Awakening"},
        {"name": "Super Metroid"},
        {"name": "Metroid Prime"},
        {"name": "Metroid Dread"},
        {"name": "Zero Mission"},
        {"name": "Castlevania Symphony of the Night"},
        {"name": "Castlevania Lords of Shadow"},
        {"name": "Bloodstained Ritual of the Night"},
        {"name": "Hollow Knight Kingdom"},
        {"name": "Blasphemous"},
        {"name": "Deaths Door"},
        {"name": "Salt and Sanctuary"},
        {"name": "Code Vein"},
        {"name": "Dark Souls"},
        {"name": "Dark Souls II"},
        {"name": "Dark Souls III"},
        {"name": "Bloodborne"},
        {"name": "Sekiro Shadows Die Twice"},
        {"name": "Armored Core VI"},
        {"name": "Monster Hunter World"},
        {"name": "Monster Hunter WorldIceborne"},
        {"name": "Monster Hunter Rise"},
        {"name": "Monster Hunter Now"},
        {"name": "God of War Ragnarok"},
        {"name": "God of War 2018"},
        {"name": "Red Dead Redemption"},
        {"name": "Red Dead Redemption 2"},
        {"name": "Grand Theft Auto VI"},
        {"name": "Grand Theft Auto V"},
        {"name": "Grand Theft Auto IV"},
        {"name": "Mafia Definitive"},
        {"name": "Mafia II"},
        {"name": "Mafia III"},
        {"name": "Sleeping Dogs"},
        {"name": "Saints Row"},
        {"name": "Saints Row 2"},
        {"name": "Saints Row The Third"},
        {"name": "Saints Row IV"},
        {"name": "Hitman"},
        {"name": "Hitman 2"},
        {"name": "Hitman 3"},
        {"name": "Splinter Cell Chaos Theory"},
        {"name": "Splinter Cell Conviction"},
        {"name": "Splinter Cell Blacklist"},
        {"name": "Metal Gear Solid V"},
        {"name": "Metal Gear Solid IV"},
        {"name": "Metal Gear Solid III"},
        {"name": "Dishonored"},
        {"name": "Dishonored Death of the Outsider"},
        {"name": "The Ninja"},
        {"name": "Assassins Creed"},
        {"name": "Assassins Creed II"},
        {"name": "Assassins Creed Brotherhood"},
        {"name": "Assassins Creed Revelations"},
        {"name": "Assassins Creed III"},
        {"name": "Assassins Creed IV Black Flag"},
        {"name": "Assassins Creed Unity"},
        {"name": "Assassins Creed Syndicate"},
        {"name": "Assassins Creed Origins"},
        {"name": "Assassins Creed Odyssey"},
        {"name": "Assassins Creed Valhalla"},
        {"name": "Assassins Creed Mirage"},
        {"name": "Tomb Raider"},
        {"name": "Rise of the Tomb Raider"},
        {"name": "Shadow of the Tomb Raider"},
        {"name": "Legend Tomb Raider"},
        {"name": "Anniversary Tomb Raider"},
        {"name": "Underworld Tomb Raider"},
        {"name": "The Last of Us"},
        {"name": "The Last of Us Part II"},
        {"name": "The Last of Us Part I"},
        {"name": "Uncharted"},
        {"name": "Uncharted 2"},
        {"name": "Uncharted 3"},
        {"name": "Uncharted 4"},
        {"name": "Uncharted Lost Legacy"},
        {"name": "Just Cause"},
        {"name": "Just Cause 2"},
        {"name": "Just Cause 3"},
        {"name": "Just Cause 4"},
        {"name": "Watch Dogs"},
        {"name": "Watch Dogs 2"},
        {"name": "Watch Dogs Legion"},
        {"name": "Prototype"},
        {"name": "Prototype 2"},
        {"name": "inFamous"},
        {"name": "inFamous 2"},
        {"name": "inFamous Second Son"},
        {"name": "Crackdown"},
        {"name": "Crackdown 2"},
        {"name": "Crackdown 3"},
        {"name": "Saints Row Reboot"},
        {"name": "Scarlet Nexus"},
        {"name": "Tales of Arise"},
        {"name": "Tales of Vesperia"},
        {"name": "Tales of Zestria"},
        {"name": "Tales of Berseria"},
        {"name": "Code Vein Battle"},
        {"name": "Soulcalibur VI"},
        {"name": "Tekken 8"},
        {"name": "Street Fighter 6"},
        {"name": "Mortal Kombat 11"},
        {"name": "Mortal Kombat 1"},
        {"name": "Guilty Gear Strive"},
        {"name": "Dragon Ball FighterZ"},
        {"name": "My Hero Academia"},
        {"name": "One Punch Man Road"},
        {"name": "Jujutsu Kaisen Cursed Clash"},
        {"name": "Demon Slayer Game"},
        {"name": "Naruto Shippuden"},
        {"name": "Bleach Soul Resonance"},
        {"name": "Attack on Titan 2"},
        {"name": "Dragon Age Inquisition"},
        {"name": "Dragon Age Origins"},
        {"name": "Baldurs Gate Dark Alliance"},
        {"name": "Neverwinter Nights"},
        {"name": "Icewind Dale"},
        {"name": "Planescape Torment"},
        {"name": "System Shock"},
        {"name": "System Shock 2"},
        {"name": "Deus Ex"},
        {"name": "Deus Ex Invisible War"},
        {"name": "Deus Ex Human Revolution"},
        {"name": "Deus Ex Mankind Divided"},
        {"name": "Bioshock"},
        {"name": "Bioshock 2"},
        {"name": "Bioshock Infinite"},
        {"name": "Crysis"},
        {"name": "Crysis 2"},
        {"name": "Crysis 3"},
        {"name": "Cryostasis"},
        {"name": "Farcry"},
        {"name": "Farcry 2"},
        {"name": "Farcry 3"},
        {"name": "Farcry 4"},
        {"name": "Farcry 5"},
        {"name": "Farcry 6"},
        {"name": "Farcry New Dawn"},
        {"name": "Borderlands"},
        {"name": "Borderlands 2"},
        {"name": "Borderlands Pre-Sequel"},
        {"name": "Tales from Borderlands"},
        {"name": "New Tales from Borderlands"},
        {"name": "The Pre-Sequel"},
        {"name": "Tiny Tinas Wonderlands"},
        {"name": "Dying Light"},
        {"name": "Dying Light 2"},
        {"name": "Dead Island"},
        {"name": "Dead Island Riptide"},
        {"name": "Mirror's Edge"},
        {"name": "Mirrors Edge Catalyst"},
        {"name": "Parkour Masters"},
        {"name": "Brink"},
        {"name": "Spec Ops The Line"},
        {"name": "F.E.A.R"},
        {"name": "F.E.A.R 2"},
        {"name": "F.E.A.R 3"},
        {"name": "Condemned Criminal Origins"},
        {"name": "Condemned 2"},
        {"name": "Killed Horizon"},
        {"name": "Horizon Zero Dawn"},
        {"name": "Horizon Forbidden West"},
        {"name": "Journey"},
        {"name": "Flower"},
        {"name": "Flow"},
        {"name": "Abzu"},
        {"name": "ICEBOUNCE"},
        {"name": "Little Big Planet"},
        {"name": "LBP 2"},
        {"name": "LBP 3"},
        {"name": "Sackboy Adventure"},
        {"name": "Knack"},
        {"name": "Knack 2"},
        {"name": "Ratchet Clank"},
        {"name": "Ratchet Clank Up Your Arsenal"},
        {"name": "Ratchet Clank Tools of Destruction"},
        {"name": "Ratchet Clank Deadlocked"},
        {"name": "Sly Cooper"},
        {"name": "Sly 2"},
        {"name": "Sly 3"},
        {"name": "Sly Cooper Thieves Return"},
        {"name": "Crash Bandicoot"},
        {"name": "Crash N.Sane Trilogy"},
        {"name": "Crash Team Racing"},
        {"name": "Spyro Year of the Dragon"},
        {"name": "Spyro Reignited Trilogy"},
        {"name": "Jak Daxter"},
        {"name": "Jak II"},
        {"name": "Jak 3"},
        {"name": "Jak X"},
        {"name": "Daxter"},
        {"name": "Halo Combat Evolved"},
        {"name": "Halo 2"},
        {"name": "Halo 3"},
        {"name": "Halo 4"},
        {"name": "Halo 5"},
        {"name": "Halo Wars"},
        {"name": "Forza Motorsport"},
        {"name": "Forza 2"},
        {"name": "Forza 3"},
        {"name": "Forza 4"},
        {"name": "Forza Motorsport 5"},
        {"name": "Forza Horizon"},
        {"name": "Forza Horizon 2"},
        {"name": "Forza Horizon 3"},
        {"name": "Forza Horizon 4"},
        {"name": "Flight Simulator 2024"},
        {"name": "Sea of Thieves"},
        {"name": "Grounded Game"},
        {"name": "Outer Wilds Echoes"},
        {"name": "A Space Adventure"},
        {"name": "Kerbal Space Program"},
        {"name": "No Mans Universe"},
        {"name": "Starfield Exploration"},
        {"name": "Star Citizen Squadron"},
        {"name": "Dual Universe"},
        {"name": "The Expanse Game"},
        {"name": "Interstellar Rift"},
        {"name": "Rodina"},
        {"name": "Universe Sandbox"},
        {"name": "Space Engine"},
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

def fetch_wikipedia_cover_image(game_name, game_folder):
    """Download cover image from Wikipedia as a fallback."""
    try:
        search_url = "https://en.wikipedia.org/wiki/Special:Search"
        response = requests.get(search_url, params={'search': game_name}, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            box = soup.find('table', {'class': 'infobox'})
            if box:
                img = box.find('img')
                if img and 'src' in img.attrs:
                    img_url = img['src']
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = 'https://en.wikipedia.org' + img_url

                    # Convert thumbnail URL to slightly larger version if possible
                    img_url = img_url.replace('/220px-', '/500px-').replace('/250px-', '/500px-')

                    img_response = requests.get(img_url, headers=HEADERS, timeout=10)
                    if img_response.status_code == 200:
                        cover_path = os.path.join(game_folder, "cover.jpg")
                        with open(cover_path, 'wb') as f:
                            f.write(img_response.content)
                        return True
        return False
    except requests.RequestException as e:
        print(f"  Wikipedia Request Error: {e}")
        return False
    except Exception as e:
        print(f"  Wikipedia Parsing Error: {e}")
        return False

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

            # Fallback to Wikipedia
            if fetch_wikipedia_cover_image(game_name, game_path):
                print("✓ Wikipedia")
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
