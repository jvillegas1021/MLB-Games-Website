from backend.python_pipelines.data_extract_functions.extract_mlb_games_info import extract_espn_mlb_games_odds, extract_mlb_games_today

from backend.python_pipelines.data_transform_functions.data_process_functions import process_mlb_games_odds_df, process_mlb_games_today_df, process_espn_mlb_games_odds_df

from backend.python_pipelines.data_load_functions.load_data_to_database import push_mlb_games_odds_data_to_sql_upsert_game_id_odds_game_id

def run_daily_mlb_games_odds_update():
    
    mlb_games_df = extract_mlb_games_today()
    if not mlb_games_df:
        print('No MLB Games Today')
        return
        
    espn_mlb_games_odds_df = extract_espn_mlb_games_odds()
    if espn_mlb_games_odds_df.empty:
        print('No MLB Games Odds Today')
        return
        
    processed_mlb_games_df = process_mlb_games_today_df(mlb_games_df)
    processed_espn_mlb_games_odds_df = process_espn_mlb_games_odds_df(espn_mlb_games_odds_df)
    mlb_games_odds_df = process_mlb_games_odds_df(processed_mlb_games_df, processed_espn_mlb_games_odds_df)

    if mlb_games_odds_df.empty:
        print('MLB Game Odds Process Failed')
        return

    
    data_table_name = 'mlb_games_odds_df'
    
    push_mlb_games_odds_data_to_sql_upsert_game_id_odds_game_id(data_table_name, mlb_games_odds_df)

if __name__ == "__main__":
    run_daily_mlb_games_odds_update()