# NAME

Alec Bawden

## DESCRIPTION

Aumni 2015-16 NBA Stats questions:

1. Which player played the third most minutes (MP) across the entire season, and how many minutes did he play?

2. Which team had the highest number of assists (AST) across all of its players?

3. Which team (TM) had the highest number of players that scored over 750 points (PTS) on the season?

4. Which player scored the highest percentage of his team's total points (PTS)?

5. Among players with at least 20 3-point field goal attempts (3PA), which player's 3-point field goal percentage (3P%) was the furthest from the average 3-point field goal percentage of their position (POS)? What was the difference?

## ASSUMPTIONS

1. Assumption made that stats are only across entire "regular" season, exclusive of Playoffs

2. Avoided using python libraries besides "Requests" library for API calls and "CSV" library to create CSVs. Libraries such as Pandas, NP, Collections, etc could be used to streamline logic

3. Dataset used did not have season stats to get totals. Multiplied Per Game stat with Games played and rounded to get Totals (May cause slight errors in totals caused by rounding)

4. Queries were run against tables created on a local instance of SQL SERVER EXPRESS using an ODBC driver to BULK INSERT the csv's
