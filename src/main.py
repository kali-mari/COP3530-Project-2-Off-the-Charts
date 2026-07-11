import sys
import os
sys.path.append(os.path.dirname(__file__))

from parser import load_data, get_feature_matrix
from cli import get_user_input, find_song
from kd_tree import build_tree, nearest_k
from max_heap import find_k_nearest

df = load_data()
matrix = get_feature_matrix(df)

# welcome screen 
print("Welcome to Off The Charts!")
print("Press Ctrl+C at any time to exit.\n")
tracks = list(enumerate(matrix))
tree = build_tree(tracks)
song_vectors = [(i, tuple(row)) for i, row in enumerate(matrix)]
structChoice = 0 # 1 = k-d tree, 2 = max heap

while True:
    print("Select search algorithm:")
    print("  1. K-d Tree")
    print("  2. Max Heap")
    choice = input("Enter 1 or 2: ").strip()

    if choice in ("1", "2"):
        structChoice = int(choice)
        break
    else:
        print(f"'{choice}' is not a valid option. Enter 1 or 2.\n")

while True:
    try:
        track_name, artist = get_user_input(df)
        song = find_song(df, track_name, artist)

        if song is not None:
            idx = song.name
            target = matrix[idx]

            # let user switch algorithm each search
            print("Select search algorithm:")
            print("  1. K-d Tree")
            print("  2. Max Heap")
            while True:
                choice = input("Enter 1 or 2: ").strip()
                if choice in ("1", "2"):
                    structChoice = int(choice)
                    break
                else:
                    print(f"'{choice}' is not a valid option. Enter 1 or 2.\n")

            if structChoice == 1:
                recommendations = nearest_k(tree, target)
            else:
                recommendations = find_k_nearest(idx, target, song_vectors)

            print("\nTop 5 similar songs:")
            for i, (rec_idx, dist) in enumerate(recommendations, 1):
                rec = df.iloc[rec_idx]
                similarity = round(100 / (1 + dist), 1)
                print(f"  {i}. {rec['track_name']} by {rec['artists']}  —  {similarity}% match")

        print()

    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)