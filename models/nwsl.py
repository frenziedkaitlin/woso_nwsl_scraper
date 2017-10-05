from pony.orm import *
from scrape import * 
from datetime import datetime
import os
from pprint import pprint
import operator 

db = Database()

class Game(db.Entity):
    id= PrimaryKey(int, auto=True)
    date= Required(datetime)
    home= Required(str)
    home_score= Required(int)
    away= Required(str)
    away_score= Required(int)
    link= Required(str)
    location= Required(str)
    attendance= Required(int)
    clearances_away= Required(int)
    clearances_home= Required(int)
    corners_away= Required(int)
    corners_home= Required(int)
    crosses_away= Required(int)
    crosses_home= Required(int)
    duels_won_away= Required(int)
    duels_won_home= Required(int)
    fouls_away= Required(int)
    fouls_home= Required(int)
    offsides_away= Required(int)
    offsides_home= Required(int)
    passing_accuracy_away= Required(int)
    passing_accuracy_home= Required(int)
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
    goals = Set('Goal')
    plays = Set('Play')
    players = Set('PlayerGame')

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
    date = Required(datetime)

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


def instantiate_nwsl():
	db.bind('sqlite', '../data/nwsl.sqlite', create_db=True)
	db.generate_mapping(create_tables=True)

def save_matches(matches):
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
        try:
            passing_accuracy_away= int(match['passing_accuracy_away'])
        except KeyError:
            passing_accuracy_away = -1
        try:
            passing_accuracy_home= int(match['passing_accuracy_home'])
        except KeyError:
            passing_accuracy_home = -1
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
                attendance = match['attendance'],
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
                            date = g.date,
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

@db_session
def get_player_stats(first, last, team, before_date, after_date=datetime.min):
    stats = []
    full_name = first +' '+ last
    player_games = select(p for p in PlayerGame 
        if p.first==first and p.last==last and p.date < before_date and p.date > after_date).order_by(desc(PlayerGame.date))

    for game in player_games[:20]:
        game_obj = select(g for g in Game if g == game.game).get()
        plays = select(p for p in Play if p.game == game.game)
        minutes = select(p.minute for p in Play if p.game == game.game)
        stat = {}
        stat['game_id'] = game_obj.id
        if game.start == -1:
            stat['minutes'] = 0
            stat['goals'] = 0
            stat['assists'] = 0
            stat['shots_on_goal'] = 0
            stat['yellows'] = 0
            stat['reds'] = 0
            stat['fouls_committed'] = 0
            stat['fouls_sufferred'] = 0
            stat['saves'] = 0
            stat['mwg'] = 0
        else:
            if game.end != -1:
                stat['minutes'] = game.end - game.start
            else:
                end = minutes.max()
                stat['minutes'] = end - game.start

            stat['goals'] = select(g for g in Goal 
                if g.player== game and game_obj==g.game).count()
            stat['shots_on_goal'] = select(p for p in Play 
                if p.game == game_obj
                and p.actor1_name==full_name 
                and (p.action=='shot_saved' or
                    p.action=='shot_blocked' or
                    p.action=='goal')).count()
            stat['all_shots'] = select(p for p in Play 
                if p.game == game_obj
                and p.actor1_name==full_name 
                and (p.action=='shot_saved' or
                    p.action=='shot_blocked' or
                    p.action=='goal' or
                    p.action=='miss')).count()
            stat['assists_attempts'] = select(p for p in Play 
                if p.game == game_obj
                and p.actor2_name==full_name 
                and (p.action=='shot_saved' or
                    p.action=='shot_blocked' or
                    p.action=='goal')).count()
            stat['assists'] = select(p for p in Play 
                if p.game == game_obj
                and p.actor2_name==full_name 
                and p.action=='goal').count()
            stat['fouls_sufferred'] =select(p for p in Play 
                if p.game == game_obj
                and p.actor1_name==full_name 
                and p.action=='free_kick_won').count()
            stat['fouls_committed'] = select(p for p in Play 
                if p.game == game_obj
                and p.actor1_name==full_name 
                and (p.action=='free_kick_lost')).count()

            #need to deal with gk subs properly but whatever for now
            stat['saves'] = 0
            if game.position == "Goalkeeper":
                stat['saves'] = select(p for p in Play 
                if p.game == game_obj
                and p.action=='shot_saved').count()
                stat['pks_saved'] = 0


            stat['reds'] = select(p for p in Play 
                if p.game == game_obj
                and p.actor1_name==full_name 
                and (p.action=='red')).count()
            stat['yellows'] =select(p for p in Play 
                if p.game == game_obj
                and p.actor1_name==full_name 
                and (p.action=='yellow')).count()


            goals = select(p for p in Play 
                if p.game == game_obj
                and p.action=='goal').order_by(Play.minute)
            teams = {}
            mwg = None
            for g in goals:
                if g.team not in teams:
                    teams[g.team] = 0
                teams[g.team] = teams[g.team] + 1
                steams = max(teams.items(), key=operator.itemgetter(1))
                if len(steams)>0 and steams[0] != steams[1]:
                    if g.team == steams[0]:
                        mwg = g
            if mwg == game:
                stat['mwg'] = 1
            else:
                stat['mwg'] = 0

            stat['pks_missed'] = 0


            if game.team == game_obj.away:
                stat['team_goals'] = game_obj.away_score
                stat['against_goals'] = game_obj.home_score
                stat['home'] = False
            else:
                stat['team_goals'] = game_obj.home_score
                stat['against_goals'] = game_obj.away_score
                stat['home'] = True

            if stat['against_goals'] == 0:
                stat['shutout'] = 1
            else:
                stat['shutout'] = 0
        stats.append(stat)
    return stats

@db_session
def get_all_matches(team):
    gs = len(select(g for g in Game if g.home==team or g.away==team))
    return select(g for g in Game if g.home==team or g.away==team)[:gs]
