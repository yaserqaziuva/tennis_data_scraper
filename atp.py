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
	player_matches = get_matches_for_player(df, player_name)
	if player_matches.empty:
		return "Please recheck the player name!"
	on_surface = player_matches[player_matches["match_surface"].str.lower().str.contains(surface)].copy()
	return on_surface

def get_all_matches_between_two_players(df, player1, player2):
	player1_matches = get_matches_for_player(df, player1)
	player2_matches = get_matches_for_player(df, player2)
	combined = pd.merge(player1_matches, player2_matches, how='inner', on=['match_id'])
	return combined

def get_head_to_head(df, player1, player2):
	matchups = get_all_matches_between_two_players(df, player1, player2)
	player1_wins = 0
	player2_wins = 0
	winners = matchups["winner_name_x"].value_counts()
	return winners.to_dict()


"""df apply functions"""
def match_surface(row, surface_dict):
	year_id = str(row["tourney_year_id"])
	return surface_dict[year_id]

def concatenate_tourney_id(row):
	return str(row["tourney_year"]) + '-' + str(row["tourney_id"])

if __name__ == "__main__":
	match_scores_old = pd.read_csv('./csv/2_match_scores/match_scores_1991-2016_UNINDEXED.csv')
	match_scores_recent = pd.read_csv('./csv/2_match_scores/match_scores_2017_UNINDEXED.csv')
	frames = [match_scores_old, match_scores_recent]
	complete = pd.concat(frames, ignore_index=True)

	tourney_data = pd.read_csv('./csv/1_tournaments/tournaments_1877-2017_UNINDEXED.csv')
	filtered_tourney_data = tourney_data[tourney_data['tourney_year'] >= 1991].copy()
	print(len(filtered_tourney_data))
	filtered_tourney_data["tourney_id"] = filtered_tourney_data["tourney_id"].astype(str).replace('\.0', '', regex=True)
	filtered_tourney_data["tourney_year_id"] = filtered_tourney_data.apply(lambda row: concatenate_tourney_id(row), axis=1)
	
	surfaces = {}
	for index, rows in filtered_tourney_data.iterrows():
		surfaces[rows["tourney_year_id"]] = rows["tourney_surface"]


	complete["match_surface"] = complete.apply(lambda row: match_surface(row, surfaces), axis=1)
	complete.to_csv(path_or_buf='./final.csv')
	match_stats_2016 = pd.read_csv('./csv/3_match_stats/match_stats_1991-2016_UNINDEXED.csv')
	match_stats_2017 = pd.read_csv('./csv/3_match_stats/match_stats_2017_UNINDEXED.csv')
	frames = [match_stats_2016, match_stats_2017]
	match_stats_concat = pd.concat(frames, ignore_index=True)
	match_stats_concat.to_csv(path_or_buf='./all_match_stats.csv')

	print(len(complete))
	print(len(match_stats_concat))

	print(get_head_to_head(complete, "nadal", "novak djokovic"))



