import os
import requests
from datetime import datetime
import time
from urllib.parse import quote
import json

BASE_GAMES_PATH = "./pc_games"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

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
    """Download cover image from Steam using app ID."""
    try:
        # Steam library header URL format
        cover_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/library_600x900_2x.jpg"

        response = requests.get(cover_url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            # Save the image
            cover_path = os.path.join(game_folder, "cover.jpg")
            with open(cover_path, 'wb') as f:
                f.write(response.content)
            return True

        # Try alternative Steam cover URL
        cover_url_alt = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
        response = requests.get(cover_url_alt, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            cover_path = os.path.join(game_folder, "cover.jpg")
            with open(cover_path, 'wb') as f:
                f.write(response.content)
            return True

        return False
    except Exception as e:
        return False


def fetch_steamgriddb_image(game_name, game_folder):
    """Download cover from SteamGridDB (no API key needed for basic search)."""
    try:
        # Search on SteamGridDB
        search_url = "https://www.steamgriddb.com/api/v2/search/autocomplete/game"
        params = {'query': game_name}

        response = requests.get(search_url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()

        results = response.json()
        if not results.get('data'):
            return False

        game_id = results['data'][0]['id']

        # Get cover image
        covers_url = f"https://www.steamgriddb.com/api/v2/grids?game_id={game_id}&dimensions=600x900"
        response = requests.get(covers_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        covers = response.json()
        if not covers.get('data'):
            return False

        # Get the first cover
        cover_data = covers['data'][0]
        image_url = cover_data['url']

        # Download image
        response = requests.get(image_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            cover_path = os.path.join(game_folder, "cover.jpg")
            with open(cover_path, 'wb') as f:
                f.write(response.content)
            return True

        return False
    except Exception as e:
        return False


def create_generic_cover(game_name, game_folder):
    """Create a generic placeholder cover image."""
    try:
        # Create a simple colored placeholder using PIL if available
        # If PIL not available, just skip
        from PIL import Image, ImageDraw, ImageFont

        # Create a simple cover image
        img = Image.new('RGB', (600, 900), color=(45, 45, 48))
        draw = ImageDraw.Draw(img)

        # Add game name
        try:
            # Try to use a built-in font
            font = ImageFont.load_default()
        except:
            font = None

        # Add text
        text_color = (200, 200, 200)
        text = game_name[:50]  # Limit text length

        if font:
            draw.text((50, 400), text, fill=text_color, font=font)
        else:
            draw.text((50, 400), text, fill=text_color)

        # Save image
        cover_path = os.path.join(game_folder, "cover.jpg")
        img.save(cover_path, 'JPEG')
        return True
    except Exception:
        return False


def download_game_covers(base_path=BASE_GAMES_PATH):
    """Download cover images for all games."""
    if not os.path.exists(base_path):
        print(f"Error: Base path does not exist: {base_path}")
        return

    game_folders = sorted([f for f in os.listdir(base_path) 
                          if os.path.isdir(os.path.join(base_path, f))])

    print(f"\nFound {len(game_folders)} game folders")
    print("=" * 70)
    print()

    steam_success = 0
    steamgrid_success = 0
    placeholder_success = 0
    failed = 0

    for idx, game_folder in enumerate(game_folders, 1):
        game_name = game_folder
        game_path = os.path.join(base_path, game_folder)
        cover_path = os.path.join(game_path, "cover.jpg")

        # Skip if cover already exists
        if os.path.exists(cover_path):
            print(f"[{idx}/{len(game_folders)}] {game_name}... ⊘ Already exists")
            continue

        try:
            print(f"[{idx}/{len(game_folders)}] {game_name}...", end=" ", flush=True)

            # Try Steam first
            app_id = fetch_steam_app_id(game_name)
            if app_id:
                if fetch_steam_cover_image(app_id, game_name, game_path):
                    print("✓ Steam")
                    steam_success += 1
                    time.sleep(0.2)
                    continue

            time.sleep(0.2)

            # Try SteamGridDB
            if fetch_steamgriddb_image(game_name, game_path):
                print("✓ SteamGridDB")
                steamgrid_success += 1
                time.sleep(0.2)
                continue

            time.sleep(0.2)

            # Create placeholder
            if create_generic_cover(game_name, game_path):
                print("◐ Placeholder")
                placeholder_success += 1
            else:
                print("✗ Failed")
                failed += 1

        except Exception as e:
            print(f"✗ Error")
            failed += 1

    print("\n" + "=" * 70)
    print("SUMMARY:")
    print(f"Downloaded from Steam: {steam_success} images")
    print(f"Downloaded from SteamGridDB: {steamgrid_success} images")
    print(f"Placeholder created: {placeholder_success} images")
    print(f"Failed: {failed} images")
    print(f"Total: {steam_success + steamgrid_success + placeholder_success + failed} images")
    print("=" * 70)


def main():
    """Main function."""
    print("=" * 70)
    print("DOWNLOAD ACTUAL GAME COVER IMAGES FROM WEB")
    print("=" * 70)
    print()

    # Get custom path
    custom_path = input(f"Enter path to game folders (default: {BASE_GAMES_PATH}): ").strip()
    if custom_path:
        base_path = custom_path
    else:
        base_path = BASE_GAMES_PATH

    print()

    # Confirm before proceeding
    confirm = input("This will download cover images from Steam/SteamGridDB. Continue? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Cancelled.")
        return

    print()

    download_game_covers(base_path)

    print("\n✓ Process complete!")
    print("\nAll game folders now contain cover.jpg files!")


if __name__ == "__main__":
    main()
