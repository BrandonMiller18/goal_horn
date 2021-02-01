import requests
import json
import time

from playsound import playsound

base_url = "https://statsapi.web.nhl.com/api/v1/"

def celebration(abr):
	"""celebration when the your team scores."""
	print(f"{abr} SCORED!!!")
	playsound(f"{abr}.mp3")

def win(abr):
	"""celebration to play when your team wins"""
	playsound(f"{abr}_win.mp3")

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
				"""Continous loop to check game score, play cellys"""
				if test:
					# data from file for testing purposes
					with open('sched.json') as f:
						data = json.load(f)
					stream_delay = 0 # no delay for testing
				else:
					r = requests.get(base_url + f"schedule?teamId={team_id}")
					data = r.json()
					stream_delay = 50 # delay for the stream

				game_status = data['dates'][0]['games'][0]['status']['abstractGameState']

				# set new scores with new data
				away_score = data['dates'][0]['games'][0]['teams']['away']['score']
				home_score = data['dates'][0]['games'][0]['teams']['home']['score']

				if i == 1: # skip on first iteration to set comparison scores
					if away:
						if away_score != away_scoreLast:
							time.sleep(stream_delay) # adjust to line up with your stream
							celebration(abr)
							# time.sleep(30)
						if home_score != home_scoreLast:
							# time.sleep(stream_delay)
							print("BAD GUYS SCORED")
							time.sleep(30)
					if home:
						if home_score != home_scoreLast:
							time.sleep(stream_delay)
							celebration(abr)
							# time.sleep(30)
						if away_score != away_scoreLast:
							# time.sleep(stream_delay)
							print("BAD GUYS SCORED")
							time.sleep(30)
				else:
					i += 1 # set i equal to 1 on first iteration

				# set last loop's scores to compare against
				away_scoreLast = away_score
				home_scoreLast = home_score
				print(home_score, away_score)

				if game_status == "Final":
					if away:
						if away_score > home_score:
							time.sleep(stream_delay)
							win(abr) # PLAY GLORIA!
					if home:
						if home_score > away_score:
							time.sleep(stream_delay)
							win(abr)
					print("GAME OVER")
					break

				time.sleep(5) # request every x seconds
				# END WHILE TRUE LOOP #

		if game_status == "Preview":
			print(f"The {abr} game has not started yet.")
	else:
		print(f"That sucks, {abr} does not play today.")

	
if __name__ == "__main__":
	abr = input("Enter the abbreviation of your favorite team: ")
	app(get_team(abr), abr)