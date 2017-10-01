import csv
import urllib
from bs4 import BeautifulSoup
import re
from pprint import pprint
from dateutil import parser

url = 'http://www.nwslsoccer.com/schedule'
root = 'https://www.nwslsoccer.com'

def get_matches(month, year):
	matches = []
	if month <10:
		month = '0' + str(month)
	else:
		month = str(month)
	path = url+'?season='+str(year)+'&month='+month
	print(path)
	soup = BeautifulSoup(urllib.request.urlopen(path).read(), 'html.parser')
	rows = soup.select('.list-row')

	date = ''
	for row in rows:
		try:
			if row.find('div', class_='played') is not None:
				columns = row.find_all("div", class_="data")
				dateobj = columns[0].find("div", class_="date")
				if dateobj.find("span", class_='dark-red') is not None:
					date = dateobj.find("span", class_='dark-red').text
				matchup = columns[1].find("div", class_="match-up")
				location = columns[1].find("div", class_="location").text.strip().replace('\n', ', ')
				teams = matchup.find_all("span", class_="short")
				scores = matchup.find_all("p", class_="score")
				if(len(teams) != 0):
					home = teams[0].text.strip()
					away = teams[1].text.strip()
					homescore = scores[0].text.strip()
					awayscore = scores[1].text.strip()
					link = columns[1].find("div", class_="call-to-action").find_all('a')[0].get('href')
					dt = parser.parse(date)

					match = get_match_data(home, away, link)
					if match is not None:
						match['date'] = dt  
						match['home'] = home
						match['away'] = away
						match['home_score'] = homescore
						match['away_score'] = awayscore
						match['location'] = location
						match['link'] = link
						matches.append(match)
		except IndexError as e:
			print(e.args)
	return matches


def get_match_data(home, away, link):
	print(home+' '+away)
	match = {}
	soup = BeautifulSoup(urllib.request.urlopen(root+link).read(), 'html.parser')
	boxscore = soup.find("div", id="boxscore")
	stats = boxscore.find('section', class_='list').find_all('div', class_='list-row')
	for stat in stats:
		cells = stat.find_all('div', class_='panel-cell')
		stat_name = str.lower(cells[1].text.strip().replace(' ', '_'))
		h = stat_name+'_home'
		a = stat_name+'_away'
		match[h]= float(cells[0].text.strip())
		match[a] = float(cells[2].text.strip())

	match['players'] = []

	lineups = soup.find("div", id="line-up").find_all("div", class_="squad")
	lins = {home: lineups[0], away: lineups[1]}
	for team, plyrs in lins.items():
		player_panels = plyrs.find_all('div', class_='panel-default')
		for player_panel in player_panels:
			position = player_panel.find_all("h5", class_="position")[0].text
			if position != "Manager":
				player = {}
				player['position'] = position
				if position == "":
					player['position'] = "Unlisted" 
				player['shirt'] = player_panel.find_all("span", class_="shirt-number")[0].text.strip()
				player['first'] = player_panel.find_all("span", class_="first-name")[0].text
				player['last'] = player_panel.find_all("span", class_="last-name")[0].text
				player['team'] = team
				player['goals'] = []
				if position != "Substitute":
					player['start_minute'] = 0
					player['end_minute'] = -1
				else:
					player['start_minute'] = -1
					player['end_minute'] = -1
				stats = player_panel.find_all("div", class_="stats")[0].text.replace('"', '').strip()
				if stats != "":
					stats = player_panel.find_all("div", class_="stats")[0].find_all('span', class_='stat')
					for stat in stats:
						if len(stat.find_all('i', class_='fa-futbol-o'))>0:
							goals = stat.text.split("'")
							for goal in goals:
								if goal.strip() != '':
									goal_o = {}
									goal_o['extra'] = -1
									goal_o['minute'] = int(goal.strip())
									goal_o['team'] = team
									player['goals'].append(goal_o)
						elif len(stat.find_all('i', class_='text-success'))>0:
							player['start_minute'] = int(stat.text.split("'")[0].strip())
						elif len(stat.find_all('i', class_='text-danger'))>0:
							player['end_minute'] = int(stat.text.split("'")[0].strip())
				match['players'].append(player)


	match['plays'] = []

	plays = soup.find("div", id="play-by-play").find_all("div", class_="play-item")
	for play_h in plays:
		minu = play_h.find("div", class_='minute')
		if minu is not None:
			minutes = minu.text.strip().split("'")
			if minutes[0] != '':
				play = {}
				play['actor_1'] = ''
				play['actor_2'] = ''	
				if len(minutes) > 1 and minutes[1]!='':
					play['extra'] = int(minutes[1].strip())
				else:
					play['extra'] = 0
				play['minute'] = int(minutes[0].strip())

				mess = play_h.find("div", class_='message')
				mtext = mess.find('p').text

				if "CORNER" in mess.find('h4'):
					play['action'] = "corner"
					play['team'] = mtext.replace('Corner,', '').split('.')[0].strip()
					#player that conceded the corner
					play['actor_1'] = mtext.split('Conceded by ')[1].replace('.', '').strip()
				elif "OFFSIDE" in mess.find('h4'):
					play['action'] = "offside"
					play['team'] = mtext.replace('Offside,', '').split('.')[0].strip()
					#player caught offside
					play['actor_1'] = mtext.split(', but ')[1].split(' is caught offside')[0].strip()
					#player whose action got the primary actor caught
					play['actor_2'] = mtext.split('.')[1].split(' tries a through ball')[0].strip()
				elif "MISS" in mess.find('h4'):
					play['action'] = "miss"
					play['team'] = mtext.split('(')[1].split(')')[0].strip()
					#person who shot
					play['actor_1'] = mtext.replace('Attempt missed. ', '').split('(')[0].strip()
					#possible assist
					if len(mtext.split('Assisted by ')) > 1:
						play['actor_2'] = mtext.split('Assisted by ')[1].split('with')[0].replace('.', '').strip()
				elif "FREE KICK LOST" in mess.find('h4'):
					play['action'] = "free_kick_lost"
					play['team'] = mtext.split('(')[1].split(')')[0].strip()
					play['actor_1'] = mtext.replace('Foul by', '').split('(')[0].strip()
				elif "ATTEMPT SAVED" in mess.find('h4'):
					play['action'] = "shot_saved"
					play['team'] = mtext.split('(')[1].split(')')[0].strip()
					#person who shot
					play['actor_1'] = mtext.replace('Attempt saved. ', '').split('(')[0].strip()
					#possible assist
					if len(mtext.split('Assisted by ')) > 1:
						play['actor_2'] = mtext.split('Assisted by ')[1].split('with')[0].replace('.', '').strip()
				elif "FREE KICK WON" in mess.find('h4'):
					play['action'] = "free_kick_won"
					play['team'] = mtext.split('(')[1].split(')')[0].strip()
					play['actor_1'] = mtext.split('(')[0].strip()
				elif "YELLOW CARD" in mess.find('h4'):
					play['action'] = "yellow"
					play['team'] = mtext.split('(')[1].split(')')[0].strip()
					play['actor_1'] = mtext.split('(')[0].strip()
				elif "RED CARD" in mess.find('h4'):
					play['action'] = "red"
					play['team'] = mtext.split('(')[1].split(')')[0].strip()
					play['actor_1'] = mtext.split('(')[0].strip()
				elif "ATTEMPT BLOCKED" in mess.find('h4'):
					play['action'] = "shot_blocked"
					play['team'] = mtext.split('(')[1].split(')')[0].strip()
					#person who shot
					play['actor_1'] = mtext.replace('Attempt blocked. ', '').split('(')[0].strip()
					#possible assisted
					if len(mtext.split('Assisted by ')) > 1:
						play['actor_2'] = mtext.split('Assisted by ')[1].split('with')[0].replace('.', '').strip()
				elif "GOAL" in mess.find('h4'):
					play['action'] = "goal"
					play['team'] = mtext.split('(')[1].split(')')[0].strip()
					#person who shot
					play['actor_1'] = mtext.split('.')[1].split('(')[0].strip()
					#possible assisted
					if len(mtext.split('Assisted by ')) > 1:
						play['actor_2'] = mtext.split('Assisted by ')[1].split('with')[0].replace('.', '').strip()
				elif "END 1" in mess.find('h4'):
					print("END 1")
				elif "END 2" in mess.find('h4'):
					print("END 2")
				# else:
				# 	print(mess.find('h4').text)
				try:
					test = play['action']
					match['plays'].append(play)
				except KeyError:
					test = 'unimportant play'
	return match