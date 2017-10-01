# NWSL Game Scraper

A script to scrape the NWSL website and save the results of each game in a database.

## Installation

To install, use pip3 to install the dependencies listed in requirements.txt. 


## Model Descriptions

### Game
* id (int)
* away (str)
* away\_score (int)
* clearances\_away (int)
* clearances\_home (int)
* corners\_away (int)
* corners\_home (int)
* crosses\_away (int)
* crosses\_home (int)
* date (datetime)
* duels\_won\_away (int)
* duels\_won\_home (int)
* fouls\_away (int)
* fouls\_home (int)
* goals (Goal)
* home (str)
* home\_score (int)
* link (str)
* location (str)
* offsides\_away (int)
* offsides\_home (int)
* passing\_accuracy\_away (int)
* passing\_accuracy\_home (int)
* plays (Play)
* players (PlayerGame)
* possession\_away (float)
* possession\_home (float)
* saves\_away (int)
* saves\_home (int)
* shots\_blocked\_away (int)
* shots\_blocked\_home (int)
* shots\_on\_goal\_away (int)
* shots\_on\_goal\_home (int)
* tackles\_won\_away (int)
* tackles\_won\_home (int)
* total\_passes\_away (int)
* total\_passes\_home (int)

### PlayerGame
* id (int)
* last (str)
* first (str)
* start (int)
* end (int)
* position (str)
* shirt (str)
* game (Game)
* team (str)
* goals (Goal)

### Goal
* id (int)
* minute (int)
* extra (int)
* player (PlayerGame)
* player\_name (str)
* team (str)
* game (Game)

### Play
* id (int)
* action (str)
* minute (int)
* extra (int)
* team (str)
* game (Game)
* actor1\_name (str) 
* actor2\_name (str) 
