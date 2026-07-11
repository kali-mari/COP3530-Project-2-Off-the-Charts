# Off The Charts

A music recommendation system that finds songs similar to a given input, ignoring popularity.

## Requirements
- Python 3.x
- pip

## Installation

1. Clone the repository
   git clone <repo-url>
   cd OffTheCharts

2. Install dependencies
   pip install pandas numpy prompt_toolkit

## Running the Program

   python src/main.py

## Usage

1. Type a song title — autocomplete will suggest matches as you type
2. Available artists for that title will be listed automatically
3. Type an artist name from the list — autocomplete is available here too
4. The top 5 most similar songs will be returned

Press Ctrl+C at any time to exit.

## Dataset

The dataset is included at data/dataset.csv and does not require any additional setup.
Source: https://doi.org/10.34740/kaggle/dsv/4372070

## Team
- Person 1: Data parsing and CLI (Kalista Oberes)
- Person 2: Max heap algorithm (Nicholas St. Onge)
- Person 3: K-d tree algorithm (Hussain Taheri)