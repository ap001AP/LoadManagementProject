import pandas as pd

# Load your CSV
df = pd.read_csv("lebron_davis_gamelogs_2023_24.csv")
df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])

# Sort by player and date
df = df.sort_values(by=['PLAYER_NAME', 'GAME_DATE'])

# Calculate days since last game
df['DAYS_SINCE_LAST_GAME'] = df.groupby('PLAYER_NAME')['GAME_DATE'].diff().dt.days

# Rolling average of minutes over last 3 games (excluding current)
df['ROLLING_MIN_AVG_3'] = df.groupby('PLAYER_NAME')['MIN'].shift(1).rolling(window=3).mean()

# Back-to-back flag (1 if played the day before)
df['BACK_TO_BACK'] = (df['DAYS_SINCE_LAST_GAME'] == 1).astype(int)

# Preview
print(df[['PLAYER_NAME', 'GAME_DATE', 'MIN', 'DAYS_SINCE_LAST_GAME', 'ROLLING_MIN_AVG_3', 'BACK_TO_BACK']].head(10))

# Save updated file
df.to_csv("fatigue_features_lebron_davis.csv", index=False)

# Calculating fatigue score per game 

# Normalize values to a 0-1 range per player
df['NORM_MIN'] = df.groupby('PLAYER_NAME')['ROLLING_MIN_AVG_3'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
df['NORM_DAYS_OFF'] = df['DAYS_SINCE_LAST_GAME'].apply(lambda x: 0 if pd.isna(x) else min(x, 5) / 5)  # 0–5 day cap
df['NORM_BACK_TO_BACK'] = df['BACK_TO_BACK']  # already 0 or 1

# Compute fatigue score: higher = more fatigue
df['FATIGUE_SCORE'] = (
    0.5 * df['NORM_MIN'] +        # high minutes = more fatigue
    0.3 * (1 - df['NORM_DAYS_OFF']) +  # fewer rest days = more fatigue
    0.2 * df['NORM_BACK_TO_BACK']     # back-to-back = more fatigue
)

# Preview
print(df[['PLAYER_NAME', 'GAME_DATE', 'MIN', 'DAYS_SINCE_LAST_GAME', 'FATIGUE_SCORE']].tail(10))

# Save it
df.to_csv("fatigue_scored_lebron_davis.csv", index=False)

