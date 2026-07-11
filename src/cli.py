from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def build_completers(df):
    title_completer = WordCompleter(
        df['track_name'].dropna().unique().tolist(),
        ignore_case=True,
        sentence=True  # treats the whole input as one search term
    )
    return title_completer

def get_user_input(df):
    title_completer = build_completers(df)

    track_name = prompt('Enter song title: ', completer=title_completer)

    # scope artist completer to songs matching that title
    title_matches = df[df['track_name'].str.lower() == track_name.strip().lower()]

    if title_matches.empty:
        return track_name.strip(), None

    # show available artists before prompting
    artists = title_matches['artists'].dropna().unique().tolist()
    print("\nArtists for that title:")
    for a in artists:
        print(f"  {a}")

    artist_completer = WordCompleter(
        title_matches['artists'].dropna().unique().tolist(),
        ignore_case=True,
        sentence=True
    )

    # loop until a valid artist is entered
    while True:
        artist = prompt(
            'Enter artist name: ',
            completer=artist_completer,
            default=''  # clears input field on each retry
        )
        artist = artist.strip()

        # check if input matches any artist for that title
        match = title_matches[
            title_matches['artists'].str.lower().str.contains(artist.lower())
        ]

        if not match.empty:
            return track_name.strip(), artist

        print(f"'{artist}' not found. Choose from the list above.")

def find_song(df, track_name, artist):
    if artist is None:
        print(f"No songs found with title '{track_name}'")
        return None

    title_matches = df[
        df['track_name'].str.lower() == track_name.lower()
    ]
    artist_matches = title_matches[
        title_matches['artists'].str.lower().str.contains(artist.lower())
    ]

    if artist_matches.empty:
        return None

    return artist_matches.iloc[0]

def display_song_traits(song):
    mode = 'Major' if song['mode'] == 1 else 'Minor'
    print(f"\n\t{song['track_name']} from {song['album_name']} by {song['artists']} ({song['track_genre']})")
    print(f"\t  dance: {song['danceability']:.2f}  energy: {song['energy']:.2f}  "
          f"valence: {song['valence']:.2f}  tempo: {song['tempo']:.1f} BPM  "
          f"loudness: {song['loudness']:.1f} dB")
    print(f"\t  acoustic: {song['acousticness']:.2f}  instrumental: {song['instrumentalness']:.2f}  "
          f"live: {song['liveness']:.2f}  speech: {song['speechiness']:.2f}  "
          f"key: {song['key']} {mode}  time: {song['time_signature']}/4")