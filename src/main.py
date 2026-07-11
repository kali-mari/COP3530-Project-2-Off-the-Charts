import sys
import os
sys.path.append(os.path.dirname(__file__))

from parser import load_data, get_feature_matrix
from cli import get_user_input, find_song

df = load_data()
matrix = get_feature_matrix(df)

# welcome screen 
print("Welcome to Off The Charts!")
print("Press Ctrl+C at any time to exit.\n")
structChoice = 0 # 1 = k-d tree, 2 = max heap

while True:
    # select an algorithim to use
    print("Select search algorithm:")
    print("  1. K-d Tree")
    print("  2. Max Heap")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        structChoice = 1
        """
        print("Building k-d tree...")
        tracks = list(enumerate(matrix))
        tree = build_tree(tracks)
        """
        print("Ready!\n")
        break
    elif choice == "2":
        structChoice = 2
        print("Ready!\n")
        break
    else:
        print(f"'{choice}' is not a valid option. Enter 1 or 2.\n")

while True:
    try:
        track_name, artist = get_user_input(df)
        song = find_song(df, track_name, artist)

        if song is not None:
            print(f"\nFound: {song['track_name']} by {song['artists']}")

            #find nearest songs, return in a list

        print()  # blank line between searches

    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)