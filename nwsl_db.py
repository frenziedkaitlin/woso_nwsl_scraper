from pony.orm import *
from datetime import datetime
import os
from nwsl_scrape import * 
from pprint import pprint

db = Database()

class Game(db.Entity):
    id= PrimaryKey(int, auto=True)
    away= Required(str)
    away_score= Required(int)
    clearances_away= Required(int)
    clearances_home= Required(int)
    corners_away= Required(int)
    corners_home= Required(int)
    crosses_away= Required(int)
    crosses_home= Required(int)
    date= Required(datetime)
    duels_won_away= Required(int)
    duels_won_home= Required(int)
    fouls_away= Required(int)
    fouls_home= Required(int)
    goals = Set('Goal')
    home= Required(str)
    home_score= Required(int)
    link= Required(str)
    location= Required(str)
    offsides_away= Required(int)
    offsides_home= Required(int)
    passing_accuracy_away= Required(int)
    passing_accuracy_home= Required(int)
    plays = Set('Play')
    players = Set('PlayerGame')
    possession_away= Required(float)
    possession_home= Required(float)
    saves_away= Required(int)
    saves_home= Required(int)
    shots_blocked_away= Required(int)
    shots_blocked_home= Required(int)
    shots_on_goal_away= Required(int)
    shots_on_goal_home= Required(int)
    tackles_won_away= Required(int)
    tackles_won_home= Required(int)
    total_passes_away= Required(int)
    total_passes_home= Required(int)

class PlayerGame(db.Entity):
    id = PrimaryKey(int, auto=True)
    last = Required(str)
    first = Required(str)
    start = Required(int)
    end = Required(int)
    position = Required(str)
    shirt = Required(str)
    game = Required(Game)
    team = Required(str)
    goals = Set('Goal')

class Goal(db.Entity):
    id = PrimaryKey(int, auto=True)
    minute = Required(int)
    extra = Required(int)
    player = Required(PlayerGame)
    player_name = Required(str)
    team = Required(str)
    game = Required(Game)

class Play(db.Entity):
    id = PrimaryKey(int, auto=True)
    action = Required(str)
    minute = Required(int)
    extra = Required(int)
    team = Required(str)
    game = Required(Game)
    actor1_name = Optional(str, nullable=True) 
    actor2_name = Optional(str, nullable=True) 

def instantiate():
	db.bind('sqlite', 'data/nwsl.sqlite', create_db=True)
	db.generate_mapping(create_tables=True)

def refresh_nwsl():
    os.remove('data/nwsl.sqlite')
    instantiate()
    years = range(2016, 2017)
    months = range(4,11)
    matches =[]
    for year in years:
        for month in months:
            matches = matches + get_matches(month, year)
    print("got matches")

    for match in matches:
        away_score= int(match['away_score'])
        clearances_away= int(match['clearances_away'])
        clearances_home= int(match['clearances_home'])
        try:
           corners_away= int(match['corners_away'])
        except KeyError:
            corners_away = -1
        try:
            corners_home= int(match['corners_home'])
        except KeyError:
            corners_home = -1
        crosses_away= int(match['crosses_away'])
        crosses_home=int(match['crosses_home'])
        date= match['date']
        duels_won_away= int(match['duels_won_away'])
        duels_won_home= int(match['duels_won_home'])
        fouls_away= int(match['fouls_away'])
        fouls_home= int(match['fouls_home'])
        home= match['home']
        home_score= int(match['home_score'])
        link= match['link']
        location= match['location']
        try:
            offsides_away= int(match['offsides_away'])
        except KeyError:
            offsides_away = -1
        try:
            offsides_home= int(match['offsides_home'])
        except KeyError:
            offsides_home = -1
        passing_accuracy_away= int(match['passing_accuracy_away'])
        passing_accuracy_home= int(match['passing_accuracy_home'])
        possession_away= match['possession_away']
        possession_home= match['possession_home']
        try:
            saves_away= int(match['saves_away'])
        except KeyError:
            saves_away = -1
        try:
            saves_home= int(match['saves_home'])
        except KeyError:
            saves_home = -1
        try:
            shots_blocked_away= int(match['shots_blocked_away'])
        except KeyError:
            shots_blocked_away = -1
        try:
            shots_blocked_home= int(match['shots_blocked_home'])
        except KeyError:
            shots_blocked_home = -1
        shots_on_goal_away= int(match['shots_on_goal_away'])
        shots_on_goal_home= int(match['shots_on_goal_home'])
        tackles_won_away= int(match['tackles_won_away'])
        tackles_won_home= int(match['tackles_won_home'])
        total_passes_away= int(match['total_passes_away'])
        total_passes_home= int(match['total_passes_home'])

        with db_session:
            g = Game(away = match['away'],
                away_score= away_score,
                clearances_away= clearances_away,
                clearances_home= clearances_home,
                corners_away= corners_away,
                corners_home= corners_home,
                crosses_away= crosses_away,
                crosses_home=crosses_home,
                date= date,
                duels_won_away= duels_won_away,
                duels_won_home= duels_won_home,
                fouls_away= fouls_away,
                fouls_home= fouls_home,
                home= home,
                home_score= home_score,
                link= link,
                location= location,
                offsides_away= offsides_away,
                offsides_home= offsides_home,
                passing_accuracy_away= passing_accuracy_away,
                passing_accuracy_home= passing_accuracy_home,
                possession_away= possession_away,
                possession_home= possession_home,
                saves_away= saves_away,
                saves_home= saves_home,
                shots_blocked_away= shots_blocked_away,
                shots_blocked_home= shots_blocked_home,
                shots_on_goal_away= shots_on_goal_away,
                shots_on_goal_home= shots_on_goal_home,
                tackles_won_away= tackles_won_away,
                tackles_won_home= tackles_won_home,
                total_passes_away= total_passes_away,
                total_passes_home= total_passes_home
            )

            for player in match['players']:
                pg = PlayerGame(first = player['first'],
                            last = player['last'],
                            team = player['team'],
                            start = player['start_minute'],
                            end = player['end_minute'],
                            game = g,
                            position = player['position'],
                            shirt = player['shirt']
                        )
                g.players.add(pg)
                for goal in player['goals']:
                    g.goals.add(
                        Goal(player=pg,
                            minute=goal['minute'],
                            extra=goal['extra'],
                            team=goal['team'],
                            player_name = player['first'] + ' ' +player['last'],
                            game = g
                            ))
            for play in match['plays']:
                g.plays.add(
                    Play(action=play['action'],
                        minute=play['minute'],
                        extra=play['extra'],
                        team=play['team'],
                        actor1_name = play['actor_1'],
                        actor2_name = play['actor_2'],
                        game = g
                        ))