def convert_team_name(team):
	if team == "KC":
		return "FCKC"
	if team == "NJ":
		return "SBFC"
	if team == "WAS":
		return "WSH"
	if team == "NC" or team=="WNY":
		return "NCC"
	else:
		return team