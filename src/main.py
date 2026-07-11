import sys
import os
sys.path.append(os.path.dirname(__file__))

from parser import load_data, get_feature_matrix
from cli import get_user_input, find_song

df = load_data()
matrix = get_feature_matrix(df)

print("Welcome to Off The Charts!")
print("Press Ctrl+C at any time to exit.\n")

while True:
    try:
        track_name, artist = get_user_input(df)
        song = find_song(df, track_name, artist)

        if song is not None:
            print(f"\nFound: {song['track_name']} by {song['artists']}")
            # hand off to Person 2 or 3 here

        print()  # blank line between searches

    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)