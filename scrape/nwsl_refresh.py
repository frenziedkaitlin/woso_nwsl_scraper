from models import * 
from .nwsl_scrape import get_matches, get_match_data
from pprint import pprint
import os

def refresh_nwsl():
    instantiate_nwsl()
    years = range(2016, 2018)
    months = range(4,11)   
    matches =[]
    print("Scraping...")
    for year in years:
        for month in months:
            matches = matches + get_matches(month, year)
    print("got all matches")
    for match in matches:
        with db_session:
            possible_match = select(g for g in Game if g.date==match['date'] and g.home==match['home'] and g.away==match['away']).first()
        if possible_match is None:
            new_match = get_match_data(match, match['home'], match['away'], match['link'], match['date'])
            if new_match is not None:
                new_matches = [new_match]
                save_matches(new_matches)
                print("Recorded new game.")

def hard_refresh_nwsl():
    if os.path.exists('../../data/nwsl.sqlite'):
        os.remove('../../data/nwsl.sqlite')
    instantiate_nwsl()
    years = range(2016, 2018)
    months = range(4,11)   
    matches =[]
    print("Scraping...")
    for year in years:
        for month in months:
            matches = matches + get_matches(month, year)
    for match in matches:
        with db_session:
            possible_match = select(g for g in Game if g.date==match['date'] and g.home==match['home'] and g.away==match['away']).first()
        if possible_match is None:
            new_match = get_match_data(match, match['home'], match['away'], match['link'], match['date'])
            if new_match is not None:
                new_matches = [new_match]
                save_matches(new_matches)
                print("Recorded new game.")
