import datetime

# weeks start on thursday
seasons = {
	2016: {
		'start': datetime.date(2016, 4, 14),
		'fifa_dates': [
			datetime.date(2016, 6, 1), 
			datetime.date(2016, 8, 4), 
			datetime.date(2016, 8, 11), 
			datetime.date(2016, 8, 18), 
			datetime.date(2016, 9, 15), 
		]
	},
	2017: {
		'start': datetime.date(2017, 4, 13),
		'fifa_dates': [
			datetime.date(2017, 6, 8), 
			datetime.date(2017, 7, 27), 
			datetime.date(2017, 9, 14), 
		]
	}
}

def calculate_week(date=(datetime.datetime.now() + datetime.timedelta(days=3))):
	rawweeks = int((date.date() - seasons[date.year]['start']).days/7) + 1
	fifa_weeks_since = 0
	for week in seasons[date.year]['fifa_dates']:
		if date.date() > week:
			fifa_weeks_since = fifa_weeks_since + 1
	return rawweeks - fifa_weeks_since

def calculate_start_date(week, year=datetime.datetime.now().date().year):
	rawstart = seasons[year]['start'] + datetime.timedelta(weeks=(week-1))
	start = rawstart
	fifa_weeks_since = 0
	for dates in seasons[year]['fifa_dates']:
		if start >= dates:
			start = start + datetime.timedelta(weeks=1)
	return start