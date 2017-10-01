from nwsl_db import instantiate, refresh_nwsl

def scrape_nwsl():
	refresh_nwsl()

def instantiate_db():
	instantiate()