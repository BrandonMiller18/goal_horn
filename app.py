import requests
import json
import time

from playsound import playsound

base_url = "https://statsapi.web.nhl.com/api/v1/"

def celebration():
	"""This should be the celebration when the Blues score.
	- Goal Song
	- Goal Horn
	- Flash lights"""

def get_team(abr):
	r = requests.get(base_url + "teams")
	data = r.json()

	for team in data['teams']:
		if team['abbreviation'] == abr:
			team_id = team['id']

	return team_id

def app(team_id, abr):

	r = requests.get(base_url + f"schedule?teamId={team_id}")
	data = r.json()

	# data from file for testing purposes
	# with open('sched.json') as f:
	# 	data = json.load(f)

	home = False
	away = False
	games = data['totalItems']

	if games > 0:
		i = 0	

		away_teamId = data['dates'][0]['games'][0]['teams']['away']['team']['id']
		home_teamId = data['dates'][0]['games'][0]['teams']['home']['team']['id']

		if home_teamId == team_id:
			home = True
			print(abr + " is the home team")

		if away_teamId == team_id:
			away = True
			print(abr + " is the away team")
		
		while True:
			# request new json to check for new score
			r = requests.get(f"https://statsapi.web.nhl.com/api/v1/schedule?teamId={team_id}")
			data = r.json()

			# data from file for testing
			# with open('sched.json') as f:
			# 	data = json.load(f)

			away_score = data['dates'][0]['games'][0]['teams']['away']['score']
			home_score = data['dates'][0]['games'][0]['teams']['home']['score']

			if i == 1:
				if away:
					if away_score != away_scoreLast:
						time.sleep(12)
						print(f"{abr} SCORED!!!")
						playsound('stl.mp3')
						break
					if home_score != home_scoreLast:
						time.sleep(12)
						print("BAD GUYS SCORED")
						break
				if home:
					if home_score != home_scoreLast:
						time.sleep(12)
						print(f"{abr} SCORED!!!")
						playsound('stl.mp3')
						break
					if away_score != away_scoreLast:
						time.sleep(12)
						print("BAD GUYS SCORED")
						break
			else:
				i += 1

			away_scoreLast = away_score
			home_scoreLast = home_score
			print(home_score, away_score)

			time.sleep(8) # request every x seconds
	else:
		print("That sucks, no game today.")

	
if __name__ == "__main__":
	abr = input("Enter the abbreviation of your favorite team: ")
	app(get_team(abr), abr)