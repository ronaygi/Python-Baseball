import os
import glob
import pandas as pd

game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'))
game_files.sort()

# Read in CSV files and load to list
game_frames = []
for game_file in game_files:
    game_frame = pd.read_csv(game_file, names=['type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', 'event'])
    game_frames.append(game_frame)

# Create DataFrame games
games = pd.concat(game_frames)

# Clean up
games.loc[games["multi5"] == '??', 'multi5'] = ''

# Get identifier, filling any gaps
identifiers = games["multi2"].str.extract(r'(.LS(\d{4})\d{5})')
identifiers = identifiers.fillna(method='ffill')
identifiers.columns = ['game_id', 'year']

# Join Together games & identifiers
games = pd.concat([games, identifiers], axis=1, sort=False)

# Fill any nulls
games = games.fillna(' ')

# Set up type column as category data type
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type'])

print(games.head())


