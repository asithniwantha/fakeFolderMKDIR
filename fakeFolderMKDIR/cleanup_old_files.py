import os

BASE_GAMES_PATH = "./pc_games"

def cleanup_cover_info_files(base_path=BASE_GAMES_PATH):
    """Remove old cover_image_info.txt files since we now have actual JPG covers."""

    if not os.path.exists(base_path):
        print(f"Error: Base path does not exist: {base_path}")
        return

    game_folders = [f for f in os.listdir(base_path) 
                   if os.path.isdir(os.path.join(base_path, f))]

    print(f"Found {len(game_folders)} game folders")
    print("=" * 70)
    print()

    removed = 0

    for idx, game_folder in enumerate(game_folders, 1):
        game_path = os.path.join(base_path, game_folder)
        info_file = os.path.join(game_path, "cover_image_info.txt")

        if os.path.exists(info_file):
            try:
                os.remove(info_file)
                print(f"[{idx}/{len(game_folders)}] {game_folder}... ✓ Removed info file")
                removed += 1
            except Exception as e:
                print(f"[{idx}/{len(game_folders)}] {game_folder}... ✗ Error: {e}")

    print("\n" + "=" * 70)
    print(f"Cleaned up: {removed} cover_image_info.txt files")
    print("=" * 70)


def main():
    print("=" * 70)
    print("CLEANUP OLD COVER IMAGE INFO FILES")
    print("=" * 70)
    print()

    confirm = input("Remove old cover_image_info.txt files? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Cancelled.")
        return

    print()

    cleanup_cover_info_files()

    print("\n✓ Cleanup complete!")
    print("\nNow each game folder contains:")
    print("  - cover.jpg (actual cover image)")
    print("  - system_requirements.txt (real Steam specs)")


if __name__ == "__main__":
    main()
