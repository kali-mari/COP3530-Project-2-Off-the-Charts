import sys
import os
sys.path.append(os.path.dirname(__file__))

from parser import load_data, get_feature_matrix
from cli import get_user_input, find_song, display_song_traits
from kd_tree import build_tree, n_nearest
from max_heap import find_k_nearest


def main():
        df = load_data()
        matrix = get_feature_matrix(df)

        print("Welcome to Off The Charts!")
        print("Press Ctrl+C at any time to exit.\n")

        print("Building data structures...")
        tracks = list(enumerate(matrix))
        tree = build_tree(tracks)
        song_vectors = [(i, tuple(row)) for i, row in enumerate(matrix)]
        print("Ready!\n")

        while True:
            try:
                track_name, artist = get_user_input(df)
                song = find_song(df, track_name, artist)

                if song is not None:
                    idx = song.name
                    target = matrix[idx]

                    print("\nSelect search algorithm:")
                    print("  1. K-d Tree")
                    print("  2. Max Heap")
                    while True:
                        
                        # user structure selection and validation
                        choice = input("Enter 1 or 2: ").strip()
                        if choice in ("1", "2"):
                            break
                        else:
                            print(f"'{choice}' is not a valid option. Enter 1 or 2.\n")

                    # display selectes song
                    display_song_traits(song)

                    if choice == "1":
                        results = n_nearest(tree, target, 6) 
                        results = [(dist, node) for dist, node in results if node.index != idx]
                        results = results[:5]
                        print("\nTop 5 similar songs (K-d Tree):")
                        for i, (dist, node) in enumerate(results, 1):
                            rec = df.iloc[node.index]
                            similarity = round(100 / (1 + dist), 1)
                            print(f"  {i}. {similarity}% match:", end="")
                            display_song_traits(rec)
                            print()
                        print("-" * 80 + "\n")
                    else:
                        results = find_k_nearest(idx, target, song_vectors)
                        print("\nTop 5 similar songs:")
                        for i, (rec_idx, dist) in enumerate(results, 1):
                            rec = df.iloc[rec_idx]
                            similarity = round(100 / (1 + dist), 1)
                            print(f"  {i}. {rec['track_name']} by {rec['artists']}  —  {similarity}% match")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                sys.exit(0)

if __name__ == "__main__":
    main()