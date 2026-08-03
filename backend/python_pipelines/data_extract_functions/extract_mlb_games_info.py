import requests
from datetime import datetime, timedelta
import statsapi
import json
import pandas as pd

def games_today(game_date=None):
    
    if game_date is None:
        game_date = datetime.today().strftime('%Y-%m-%d')

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={game_date}&hydrate=probablePitcher(note)"
    today_games_data = requests.get(url).json()

    # Check if 'dates' key exists and has games
    if 'dates' not in today_games_data or not today_games_data['dates']:
        return pd.DataFrame()  # Return empty DataFrame

    todays_games_df = pd.json_normalize(today_games_data['dates'][0]['games'])
    todays_games_df.set_index('gamePk', drop=False, inplace=True)

    return todays_games_df

def games_today_with_probable_pitchers_ids(game_date = None):
    if game_date is None:
        game_date = datetime.today().strftime('%Y-%m-%d')

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={game_date}&hydrate=probablePitcher(note)"
    
    today_games_data = requests.get(url).json()

    if 'dates' not in today_games_data or not today_games_data['dates']:
        return []
    
    game_obj = today_games_data['dates'][0]['games']
    
    starting_pitcher_ids = []
    
    for game in game_obj:

        away_pp = game['teams']['away'].get('probablePitcher')
        home_pp = game['teams']['home'].get('probablePitcher')

        away_id = away_pp.get('id') if away_pp else 'TBD'
        home_id = home_pp.get('id') if home_pp else 'TBD'
        
        starting_pitcher_ids.append(away_id)
        starting_pitcher_ids.append(home_id)
        
    return starting_pitcher_ids
    
def games_today_with_pitchers(team_id: int) -> list[int]:
    url = f'https://statsapi.mlb.com/api/v1/teams/{team_id}/roster?rosterType=active'
    data = requests.get(url).json()

    bullpen = [
        pitcher["person"]["id"]
        for pitcher in data["roster"]
        if pitcher["position"]["type"] == "Pitcher"
    ]
    return bullpen

def games_today_with_teams_and_lineups_and_bullpens(game_date = None) -> list[tuple[str, int, list[int], list[int]]]:

    if game_date is None:
        game_date = datetime.now().strftime("%Y-%m-%d")

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={game_date}&hydrate=lineups"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    games_today = response.json()

    # Covers None, {}, [], "", 0
    if not games_today:
        return []

    # MLB-specific: no games scheduled
    if games_today.get("dates") == []:
        return []


    teams_playing = []

    for game in range(len(games_today['dates'][0]['games'])):
        game_obj = games_today['dates'][0]['games'][game]


        # Skip All-Star Game or any non-regular-season game
        if game_obj.get('gameType') in ('A', 'E'):
            continue

        game_id = game_obj['gamePk']
        game_official_date = game_obj['officialDate']
        
        lineups = game_obj.get('lineups')
        # If no lineups at all, skip this game
        if not lineups:
            continue
    
        # -------------------------
        # AWAY TEAM
        # -------------------------
        away_team = game_obj['teams']['away']['team']
        away_name = away_team['name']
        away_id = away_team['id']
    
        away_lineup = []
        if 'awayPlayers' in lineups:
            for p in lineups['awayPlayers']:
                away_lineup.append(p['id'])
        else:
            continue  # away lineup not hydrated yet
    
        away_bullpen = games_today_with_pitchers(away_id)
        teams_playing.append((game_id, game_official_date, away_name, away_id, away_lineup, away_bullpen))
    
        # -------------------------
        # HOME TEAM
        # -------------------------
        home_team = game_obj['teams']['home']['team']
        home_name = home_team['name']
        home_id = home_team['id']
    
        home_lineup = []
        if 'homePlayers' in lineups:
            for p in lineups['homePlayers']:
                home_lineup.append(p['id'])
        else:
            continue  # home lineup not hydrated yet
    
        home_bullpen = games_today_with_pitchers(home_id)
        teams_playing.append((game_id, game_official_date, home_name, home_id, home_lineup, home_bullpen))
    
    return teams_playing


def extract_todays_games_schedule(game_date=None) :
    if game_date is None:
        game_date = datetime.now().strftime("%Y-%m-%d")
        
    schedule = statsapi.schedule(date=game_date, start_date=None, end_date=None, team="", opponent="", sportId=1, game_id=None, season=None,
                                 include_series_status=True)
    todays_games_df = pd.json_normalize(schedule)
    
    home_team_df = todays_games_df[
        ['home_name', 'home_id', 'game_datetime', 'game_date', 'game_type', 'venue_id', 'venue_name', 'summary']
    ].copy()
    
    home_team_df['home_away'] = 'home'
    home_team_df = home_team_df.rename(columns={'home_name': 'team_name', 'home_id': 'team_id'})
    
    
    away_team_df = todays_games_df[
        ['away_name', 'away_id', 'game_datetime', 'game_date', 'game_type', 'venue_id', 'venue_name', 'summary']
    ].copy()
    
    away_team_df['home_away'] = 'away'
    away_team_df = away_team_df.rename(columns={'away_name': 'team_name', 'away_id': 'team_id'})
    
    
    combined_team_df = pd.concat([home_team_df, away_team_df], ignore_index=True)
    
    return combined_team_df

def get_current_pitcher_ids():
    pitcher_ids = set()


    # 1. Get all MLB teams
    teams = requests.get("https://statsapi.mlb.com/api/v1/teams?sportId=1").json()["teams"]

    for team in teams:
        team_id = team["id"]

        # 2. Get roster for each team
        roster_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
        roster = requests.get(roster_url).json()["roster"]

        # 3. Filter pitchers
        for player in roster:
            if player["position"]["type"] == "Pitcher" or player["position"]["type"] == "Two-Way Player":
                pitcher_ids.add(player["person"]["id"])


    return (pitcher_ids)

def get_pitcher_info_and_stats_season(pitcher_id, season=2026):
    url = f"https://statsapi.mlb.com/api/v1/people/{pitcher_id}/stats"
    params = {
        "stats": "season",
        "group": "pitching",
        "season": season
    }

    request = requests.get(url, params=params).json()

    # If request failed or empty
    if not request:
        return None

    # Guard: stats list missing or empty
    stats_list = request.get('stats', [])
    if not stats_list:
        return None

    # Guard: splits missing or empty
    splits = stats_list[0].get('splits', [])
    if not splits:
        return None

    # Safe to access now
    pitcher_details = splits[0]

    # Safe extraction
    player_info = pitcher_details.get('player', {})
    team_info = pitcher_details.get('team', {})

    pitcher_df = pd.DataFrame({
        'xMLBAMID': [player_info.get('id')],
        'player_name': [player_info.get('fullName')],
        'team_id': [team_info.get('id')],  # None if missing
        'team_name': [team_info.get('name')],  # None if missing
        'season': [pitcher_details.get('season')]
    })

    # Normalize stat block
    pitcher_details_normalize = pd.json_normalize(pitcher_details['stat'])

    # Combine horizontally
    pitcher_df = pd.concat([pitcher_df, pitcher_details_normalize], axis=1)

    return pitcher_df

def get_current_batter_ids():

    batter_ids = set()

    # 1. Get all MLB teams
    teams = requests.get("https://statsapi.mlb.com/api/v1/teams?sportId=1").json()["teams"]

    for team in teams:
        team_id = team["id"]

        # 2. Get roster for each team
        roster_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
        roster = requests.get(roster_url).json()["roster"]

        # 3. Filter pitchers
        for player in roster:
            if player["position"]["type"] != "Pitcher":
                batter_ids.add(player["person"]["id"])


    return (batter_ids)

def get_batter_info_and_stats_season(batter_id, season=2026):
    url = f"https://statsapi.mlb.com/api/v1/people/{batter_id}/stats"
    params = {
        "stats": "season",
        "group": "hitting",
        "season": season
    }

    request = requests.get(url, params=params).json()

    # If request failed or empty
    if not request:
        return None

    # Guard: stats list missing or empty
    stats_list = request.get('stats', [])
    if not stats_list:
        return None

    # Guard: splits missing or empty
    splits = stats_list[0].get('splits', [])
    if not splits:
        return None

    # Safe to access now
    batter_details = splits[0]

    # Safe extraction
    player_info = batter_details.get('player', {})
    team_info = batter_details.get('team', {})

    batter_df = pd.DataFrame({
        'xMLBAMID': [player_info.get('id')],
        'player_name': [player_info.get('fullName')],
        'team_id': [team_info.get('id')],  # None if missing
        'team_name': [team_info.get('name')],  # None if missing
        'season': [batter_details.get('season')]
    })

    # Normalize stat block
    batter_details_normalize = pd.json_normalize(batter_details['stat'])

    # Combine horizontally
    batter_df = pd.concat([batter_df, batter_details_normalize], axis=1)

    return batter_df

def get_mlb_team_record_info(league_id, year = datetime.now().year):
    url = f"https://statsapi.mlb.com/api/v1/standings?leagueId={league_id}&seasons={year}"
    request = requests.get(url).json()
    league_df = request
    return (league_df)

def extract_mlb_games_today(game_date=None):
    
    
    if game_date is None:
        game_date = datetime.today().strftime('%Y-%m-%d')
    else:
        game_date = pd.to_datetime(game_date).strftime('%Y-%m-%d')
    
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={game_date}&hydrate=probablePitcher(note)"
    
    today_games_data = requests.get(url).json()
    
    if 'dates' not in today_games_data or not today_games_data['dates']:
        return []
        
    game_obj = today_games_data['dates'][0]['games']
    
    game_ids = []
    game_date_times = []
    game_dates = []
    game_status_codes = []
    away_teams = []
    home_teams = []
    game_numbers = []
    
    for game in range(0, len(game_obj)):
        matchup = game_obj[game]
    
        game_ids.append(matchup.get('gamePk'))
        game_date_times.append(matchup.get('gameDate'))
        game_dates.append(matchup.get('officialDate'))

        game_status = matchup['status']
        game_status_codes.append(game_status.get('abstractGameCode'))
        
        away_team = matchup['teams']['away']['team']
    
        away_teams.append(away_team.get('name'))
    
        home_team = matchup['teams']['home']['team']
    
        home_teams.append(home_team.get('name'))
    
        game_numbers.append(matchup.get('gameNumber'))
    
    matchups_df = pd.DataFrame({
        'game_id': game_ids,
        'game_date_time': game_date_times,
        'game_date': game_dates,
        'game_status_code': game_status_codes,
        'away_team': away_teams,
        'home_team': home_teams,
        'game_number': game_numbers})

    matchups_df = matchups_df.sort_values('game_date_time')

    matchups_df['team_name_key'] = (
            matchups_df['away_team'] + " - " + matchups_df['home_team']
    )
    matchups_df['game_count'] = matchups_df.groupby('team_name_key').cumcount() + 1
    
    return matchups_df

def extract_espn_mlb_games_odds(game_date=None):
    
    
    if game_date is None:
        game_date = datetime.today().strftime('%Y%m%d')
    else:
        game_date = pd.to_datetime(game_date).strftime('%Y%m%d')

    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={game_date}"
    
    raw = requests.get(url).json()

    if "events" not in raw or not raw["events"]:
        return pd.DataFrame()

    odds_df = pd.json_normalize(
        raw["events"])
    
    
    game_ids = []
    dates = []
    stadiums = []
    statuses = []
    away_teams = []
    away_team_abvs = []
    home_teams = []
    home_team_abvs = []
    details = []
    over_unders = []
    spreads = []
    away_open_odds = []
    away_close_odds = []
    home_open_odds = []
    home_close_odds = []
    
    for game in range(len(odds_df['competitions'])):
        matchup = odds_df['competitions'][game][0]
    
        game_ids.append(matchup.get('id'))
        dates.append(matchup.get('date'))
    
        venue = matchup['venue']
        stadiums.append(venue.get('fullName'))

        status = matchup['status']['type']
        statuses.append(status.get('description'))
    
        away_team = matchup['competitors'][1]['team']
        home_team = matchup['competitors'][0]['team']
                        
        away_teams.append(away_team.get('displayName'))
        away_team_abvs.append(away_team.get('abbreviation'))
        
        home_teams.append(home_team.get('displayName'))
        home_team_abvs.append(home_team.get('abbreviation'))

        odds_list = matchup.get('odds', [])
    
        if odds_list:
            odds = odds_list[0]
        
            details.append(odds.get('details'))
            over_unders.append(odds.get('overUnder'))
            spreads.append(odds.get('spread'))
        
            # moneyline may also be missing
            moneyline = odds.get('moneyline', {})
        
            away_ml = moneyline.get('away', {})
            home_ml = moneyline.get('home', {})
        
            away_open_odds.append(away_ml.get('open', {}).get('odds', 0))
            away_close_odds.append(away_ml.get('close', {}).get('odds', 0))
        
            home_open_odds.append(home_ml.get('open', {}).get('odds', 0))
            home_close_odds.append(home_ml.get('close', {}).get('odds', 0))
        
        else:
            # game started OR ESPN didn’t publish odds yet
            details.append(0)
            over_unders.append(0)
            spreads.append(0)
        
            away_open_odds.append(0)
            away_close_odds.append(0)
            home_open_odds.append(0)
            home_close_odds.append(0)
    
    
        
        
    odds_final_df = pd.DataFrame({
        'odds_game_id': game_ids,
        'date_time': dates,
        'venue': stadiums,
        'status': statuses,
        'away_team_name': away_teams,
        'away_team_abv': away_team_abvs,
        'away_open_odds': away_open_odds,
        'away_close_odds': away_close_odds,
        'home_team_name': home_teams,
        'home_team_abv': home_team_abvs,
        'home_open_odds': home_open_odds,
        'home_close_odds': home_close_odds,
        'details': details,
        'over_under': over_unders,
        'spread': spreads,
        }) 

    
    odds_final_df['abv_key'] = (
        odds_final_df['away_team_abv'] + " - " + odds_final_df['home_team_abv']
    )
    odds_final_df['game_count'] = odds_final_df.groupby('abv_key').cumcount() + 1
    
    odds_final_df['away_open_odds'] = pd.to_numeric(odds_final_df['away_open_odds'], errors='coerce')
    odds_final_df['away_close_odds'] = pd.to_numeric(odds_final_df['away_close_odds'], errors='coerce')
    odds_final_df['home_open_odds'] = pd.to_numeric(odds_final_df['home_open_odds'], errors='coerce')
    odds_final_df['home_close_odds'] = pd.to_numeric(odds_final_df['home_close_odds'], errors='coerce')

    odds_final_df = odds_final_df.fillna(0)
    
    return(odds_final_df)
