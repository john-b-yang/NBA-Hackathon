# NBA-Hackathon
Answers to 2018 NBA Hackathon Application questions

Trello Task Board: https://trello.com/b/QoOLLycE

Reference Techniques:
- One Hot Encoding (MultiLabelBinarizer): Refactor team names and country labels into vector of binary values

# Approaches

1. Predict total viewership based solely on training set data (Season, Game Date, Teams)

Data Set | Original Data Set | New Columns | Removed Columns
train_1 | Training Data Set | Total Viewers | Country, Country Viewers
train_2 | train_1 | Teams (One Hot Encoded) | Away Team, Home Team, Game_ID
