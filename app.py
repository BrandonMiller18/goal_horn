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
	test = True # set to True to test with local json files

	if test:
		# data from file for testing purposes
		with open('sched.json') as f:
			data = json.load(f)
	else:
		r = requests.get(base_url + f"schedule?teamId={team_id}")
		data = r.json()

	# data from file for testing purposes
	with open('sched.json') as f:
		data = json.load(f)

	home = False
	away = False
	games = data['totalItems']

	"""Here the fun begins...if there is a game, check status. If status is 'Live'
	then we keep checking the score."""
	if games > 0:
		game_status = data['dates'][0]['games'][0]['status']['abstractGameState']
		if game_status == "Live":
			i = 0	

			away_teamId = data['dates'][0]['games'][0]['teams']['away']['team']['id']
			home_teamId = data['dates'][0]['games'][0]['teams']['home']['team']['id']

			if home_teamId == team_id: # set home or away for the team you picked
				home = True
			if away_teamId == team_id:
				away = True

			while True:
				if test:
					# data from file for testing purposes
					with open('sched.json') as f:
						data = json.load(f)
				else:
					r = requests.get(base_url + f"schedule?teamId={team_id}")
					data = r.json()

				game_status = data['dates'][0]['games'][0]['status']['abstractGameState']

				# set new scores with new data
				away_score = data['dates'][0]['games'][0]['teams']['away']['score']
				home_score = data['dates'][0]['games'][0]['teams']['home']['score']

				if i == 1: # skip on first iteration to set comparison scores
					if away:
						if away_score != away_scoreLast:
							# time.sleep(10) # adjust to line up with your stream
							print(f"{abr} SCORED!!!")
							playsound(f"{abr}.mp3")
							# time.sleep(30)
						if home_score != home_scoreLast:
							# time.sleep(10)
							print("BAD GUYS SCORED")
							# time.sleep(30)
					if home:
						if home_score != home_scoreLast:
							# time.sleep(10)
							print(f"{abr} SCORED!!!")
							playsound(f"{abr}.mp3")
							# time.sleep(30)
						if away_score != away_scoreLast:
							# time.sleep(10)
							print("BAD GUYS SCORED")
							# time.sleep(30)
				else:
					i += 1 # set i equal to 1 on first iteration

				# set last loop's scores to compare against
				away_scoreLast = away_score
				home_scoreLast = home_score
				print(home_score, away_score)

				if game_status == "Final":
					if away:
						if away_score > home_score:
							playsound(f"{abr}_win.mp3") # PLAY GLORIA!
					if home:
						if home_score > away_score:
							playsound(f"{abr}_win.mp3")
					print("GAME OVER")
					break


				time.sleep(8) # request every x seconds


		if game_status == "Preview":
			print(f"The {abr} game has not started yet.")
	else:
		print(f"That sucks, {abr} does not play today.")

	
if __name__ == "__main__":
	abr = input("Enter the abbreviation of your favorite team: ")
	app(get_team(abr), abr)