import pandas as pd

csvResults = pd.read_csv('https://football-data.co.uk/mmz4281/2425/E0.csv')

# Renaming columns
csvResults.rename(columns={'FTHG':'home_goals',
                           'FTAG':'away_goals'}, inplace=True)