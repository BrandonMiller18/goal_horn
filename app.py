import requests
import json
import time
from playsound import playsound
from config import Config

base_url = Config.base_url


def app(abr, test, team_id, stream_delay, data):


	def celebration(abr):
		"""celebration when the your team scores."""
		print(f"\n\n{abr} SCORED!!!\n\n")
		playsound(f"{abr}.mp3")


	def win(abr):
		"""celebration to play when your team wins"""
		print(f"\n\n{abr} WINS!!!\n\n")
		playsound(f"{abr}_win.mp3")


	home = False
	away = False
	games = data['totalItems']

	"""Here the fun begins...if there is a game, check status. If status is 'Live'
	then we keep checking the score."""
	while games > 0:
		data = config.data(test)	
		game_status = data['dates'][0]['games'][0]['status']['abstractGameState']

		if game_status == "Preview":
			print("Waiting for puck drop...")
			# time.sleep(60) # wait and re-check data


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
				data = config.data(test)

				game_status = data['dates'][0]['games'][0]['status']['abstractGameState']

				# set new scores with new data
				away_score = data['dates'][0]['games'][0]['teams']['away']['score']
				home_score = data['dates'][0]['games'][0]['teams']['home']['score']

				if i == 1: # skip on first iteration to set comparison scores
					if away:
						if away_score != away_scoreLast:
							time.sleep(stream_delay) # adjust to line up with your stream
							celebration(abr)
						if home_score != home_scoreLast:
							time.sleep(stream_delay)
							print("BAD GUYS SCORED")
					if home:
						if home_score != home_scoreLast:
							time.sleep(stream_delay)
							celebration(abr)
						if away_score != away_scoreLast:
							time.sleep(stream_delay)
							print("BAD GUYS SCORED")
				else:
					print("\n\nGAME START!\n\n")
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

				time.sleep(2) # request every x seconds
				# END WHILE TRUE LOOP #


		time.sleep(30)



	else:
		print(f"That sucks, {abr} does not play today.")

	
if __name__ == "__main__":
	
	abr = input("Please enter the abbreviation of your favorite team! ").upper()
	config = Config(abr)

	test = config.test()
	team_id = config.get_team(abr)
	stream_delay = config.stream_delay(test)
	data = config.data(test)

	app(abr, test, team_id, stream_delay, data)