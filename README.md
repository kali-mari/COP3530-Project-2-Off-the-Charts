# Off The Charts

```
 _____  __  __ _____ _          _____ _                _       
|  _  |/ _|/ _|_   _| |        /  __ \ |              | |      
| | | | |_| |_  | | | |__   ___| /  \/ |__   __ _ _ __| |_ ___ 
| | | |  _|  _| | | | '_ \ / _ \ |   | '_ \ / _` | '__| __/ __|
\ \_/ / | | |   | | | | | |  __/ \__/\ | | | (_| | |  | |_\__ \
 \___/|_| |_|   \_/ |_| |_|\___|\____/_| |_|\__,_|_|   \__|___/
```
♫⋆｡♪ ₊˚♬ﾟ. Find your sound. Skip the charts. ♫⋆｡♪ ₊˚♬ﾟ.

## Requirements
- Python 3.x
- pip

## Installation

1. Clone the repository
```
   git clone <repo-url>
   cd COP3530-Project-2-Off-the-Charts
```

2. Install dependencies
```
   pip install pandas numpy prompt_toolkit
```

## Running the Program
```
python src/main.py
```

## Usage

1. Type a song title — autocomplete will suggest matches as you type
2. Available artists for that title will be listed automatically
3. Type an artist name from the list — autocomplete is available here too
4. Select K-d Tree or Max Heap as the search algorithm
5. The top 5 most similar songs will be returned with trait comparisons

Press Ctrl+C at any time to exit.

## Dataset

The dataset is included at data/dataset_clean.csv and does not require any additional setup.
Source: https://doi.org/10.34740/kaggle/dsv/4372070

## Team
- Person 1: Data parsing and CLI (Kalista Oberes)
- Person 2: Max heap algorithm (Nicholas St. Onge)
- Person 3: K-d tree algorithm (Hussain Taheri)