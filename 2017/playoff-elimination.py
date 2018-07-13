import pandas as pd
import numpy as np

# Data Configuration
division_info = pd.read_excel("Analytics_Attachment.xlsx", sheetname="Division_Info")
scores = pd.read_excel("Analytics_Attachment.xlsx", sheetname="2016_17_NBA_Scores")

# For our purposes, the 'division' columns in division_info and 'Home Score', 'Away Score'
# columns in scores are unnecessary
division_info.drop('Division_id', axis=1, inplace=True)
scores.drop(['Home Score', 'Away Score'], axis=1, inplace=True)

division_info['Wins'] = 0
division_info['Losses'] = 0
division_info['Elimination Date'] = "Playoffs"

# Using a MultiIndex Pandas Dataframe, we group the games occuring on the same with each
# other to make traversal easier. The reason a 'Dummy' column is b/c multiple index groups
# are required.
scores['Game No.'] = range(0, scores['Date'].count())
scores.set_index(['Date', 'Game No.'], inplace=True)
# scores.reset_index(level=2, drop=True) # Would destory multiindex property

# Iterating through the MultiIndex Dataframe by Date
for value in scores.index.get_level_values('Date').unique():
    # Converting the TimeStamp object into a string
    currentDate = value.strftime('%Y-%m-%d')
    # Extracting the miniFrame associated with currentDate
    miniFrame = scores.xs(currentDate)

    # Iterate through all games that occurred on 'currentDate' and adjust records accordingly
    for index, row in miniFrame.iterrows():
        if (row['Winner'] == 'Home'):
            # If the home team won, look up the key in the division_info dataframe and iterate its number of wins
            division_info.loc[division_info['Team_Name'] == row['Home Team'], 'Wins'] += 1
            division_info.loc[division_info['Team_Name'] == row['Away Team'], 'Losses'] += 1
        elif (row['Winner'] == 'Away'):
            # Same thing but the other way around
            division_info.loc[division_info['Team_Name'] == row['Home Team'], 'Losses'] += 1
            division_info.loc[division_info['Team_Name'] == row['Away Team'], 'Wins'] += 1
        else:
            # Catch all case for errant values in data set
            print("Error: Invalid 'Winner' Value")

    # Elimination Calculation
    # Divide the data set into the eastern and western conference with teams that haven't been eliminated from Playoffs
    # Sort the data set by most wins in descending order
    eastern_Conference = division_info[(division_info['Conference_id'] == 'East') & (division_info['Elimination Date'] == "Playoffs")].sort_values(['Wins'], ascending=False)
    western_Conference = division_info[(division_info['Conference_id'] == 'West') & (division_info['Elimination Date'] == "Playoffs")].sort_values(['Wins'], ascending=False)

    # Identify the rows of the last place teams in each conference by most number of losses
    eastLast = eastern_Conference[eastern_Conference['Losses'] == max(eastern_Conference['Losses'])]
    westLast = western_Conference[western_Conference['Losses'] == max(western_Conference['Losses'])]

    # Identify the rows of the eighth seeds
    eastEighth = eastern_Conference.iloc[[7]]
    westEighth = western_Conference.iloc[[7]]

    # Playoff Elimination Logic: If (last seed wins + remaining games) < 8th seed wins, the last seed is eliminated.
    maxWins = eastLast['Wins'].values[0] + (82 - eastLast['Wins'].values[0] - eastLast['Losses'].values[0])
    if (eastEighth['Wins'].values[0] > maxWins):
        division_info.loc[division_info['Team_Name'] == eastLast['Team_Name'].values[0], ['Elimination Date']] = currentDate

    maxWins = westLast['Wins'].values[0] + (82 - westLast['Wins'].values[0] - westLast['Losses'].values[0])
    if (westEighth['Wins'].values[0] > maxWins):
        division_info.loc[division_info['Team_Name'] == westLast['Team_Name'].values[0], ['Elimination Date']] = currentDate

# Display the results
print(division_info.sort_values(['Conference_id', 'Wins'], ascending=False))
