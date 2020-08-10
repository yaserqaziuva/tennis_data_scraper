import datapackage
import pandas as pd

def get_matches_for_player(df, player_name):
	player_name = player_name.lower()
	player_matches = df[df['winner_name'].str.lower().str.contains(player_name) | df['loser_name'].str.lower().str.contains(player_name)].copy()
	if len(player_matches.index) == 0:
		return pd.DataFrame()
	else:
		return player_matches

def percentage_matches_won(df, player_name):
	player_matches = get_matches_for_player(df, player_name)
	if player_matches.empty:
		return "Please recheck the player name!"
	matches_won = df[df['winner_name'].str.lower().str.contains(player_name)].copy()
	return len(matches_won.index) / len(player_matches.index)

def get_matches_for_player_on_surface(df, player_name, surface):
	pass

def match_surface(row, df):
	tourney_year_id_process = str(row["tourney_year_id"])
	tourney_year_id_process = tourney_year_id_process.split('-')
	tourney_year, tourney_id = int(tourney_year_id_process[0]), int(tourney_year_id_process[1])
	relevant_row = df[(df['tourney_year'] == tourney_year) & (df['tourney_id'] == tourney_id)].copy()
	tourney_surface = relevant_row['tourney_surface']
	return tourney_surface

if __name__ == "__main__":
	match_scores_old = pd.read_csv('./csv/2_match_scores/match_scores_1991-2016_UNINDEXED.csv')
	match_scores_recent = pd.read_csv('./csv/2_match_scores/match_scores_2017_UNINDEXED.csv')
	frames = [match_scores_old, match_scores_recent]
	complete = pd.concat(frames)

	tourney_data = pd.read_csv('./csv/1_tournaments/tournaments_1877-2017_UNINDEXED.csv')
	filtered_tourney_data = tourney_data[tourney_data['tourney_year'] >= 1991].copy()

	complete['match_surface'] = complete.apply(lambda row: match_surface(row, filtered_tourney_data), axis=1)
	
	



