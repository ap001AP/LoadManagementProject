from nba_api.stats.endpoints import playergamelog 
from nba_api.stats.static import players
import pandas as pd 

# List of player names
player_names = ["LeBron James", "Anthony Davis"]

# Get player ID
def get_player_id(full_name):
    return players.find_players_by_full_name(full_name)[0]['id']

# Dictionary to store dataframes
player_logs = {}

# Loop through each player
for name in player_names:
    player_id = get_player_id(name)
    gamelog = playergamelog.PlayerGameLog(
        player_id=player_id,
        season='2023-24',
        season_type_all_star='Regular Season'
    )
    df = gamelog.get_data_frames()[0]
    
    # Add player name to dataframe
    df['PLAYER_NAME'] = name
    
    # Convert game date to datetime
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    
    # Keep useful columns only
    df = df[['PLAYER_NAME', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'PTS', 'REB', 'AST']]
    
    # Store in dictionary
    player_logs[name] = df

# Combine all player logs into one DataFrame
combined_df = pd.concat(player_logs.values(), ignore_index=True)

# Save to CSV
combined_df.to_csv('lebron_davis_gamelogs_2023_24.csv', index=False)

print(combined_df.head())
