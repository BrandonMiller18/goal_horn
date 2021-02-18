import requests
import json
import time
from playsound import playsound
from config import *


def watch_game():

	test = game.test
	abr = game.abr
	team_id = game.team_id
	stream_delay = game.stream_delay
	data = game.data

	def refresh_data():
		data = game.get_data(test, team_id)
		return data


	def celebration():
		"""celebration when the your team scores."""
		print(f"\n\n{abr} SCORED!!!\n\n")
		playsound(f"{abr}.mp3")


	def win():
		"""celebration to play when your team wins"""
		print(f"\n\n{abr} WINS!!!\n\n")
		playsound(f"{abr}_win.mp3")

	home = False
	away = False
	games = data['totalItems']

	"""Here the fun begins...if there is a game, check status. If status is 'Live'
	then we keep checking the score."""
	while games > 0:
		data = refresh_data()
		game_status = data['dates'][0]['games'][0]['status']['abstractGameState']

		if game_status == "Preview":
			game_status = data['dates'][0]['games'][0]['status']['abstractGameState']
			print("Waiting for puck drop.")
			time.sleep(1)
			print("Waiting for puck drop..")
			time.sleep(1)
			print("Waiting for puck drop...")
			time.sleep(10)
			print("\n\nCHECKING STATUS\n")


		elif game_status == "Live":

			away_teamId = data['dates'][0]['games'][0]['teams']['away']['team']['id']
			home_teamId = data['dates'][0]['games'][0]['teams']['home']['team']['id']

			if home_teamId == team_id: # set home or away for the team you picked
				home = True
				print(f"----------\n----------\nThe puck has dropped at {team.venue}!\n")
			if away_teamId == team_id:
				away = True
				print("----------\n----------\nThe puck has dropped!\n")

			i = 0	

			while game_status == "Live":
				"""Continous loop to check game score, play cellys"""
				data = refresh_data()

				game_status = data['dates'][0]['games'][0]['status']['abstractGameState']

				# set new scores with new data
				away_score = data['dates'][0]['games'][0]['teams']['away']['score']
				home_score = data['dates'][0]['games'][0]['teams']['home']['score']

				if i == 1: # skip on first iteration to set comparison scores
					if away:
						if away_score != away_scoreLast:
							time.sleep(stream_delay) # adjust to line up with your stream
							celebration()
						if home_score != home_scoreLast:
							time.sleep(stream_delay)
							print("BAD GUYS SCORED")
					if home:
						if home_score != home_scoreLast:
							time.sleep(stream_delay)
							celebration()
						if away_score != away_scoreLast:
							time.sleep(stream_delay)
							print("BAD GUYS SCORED")
				else:
					i += 1 # set i equal to 1 on first iteration

				# set last loop's scores to compare against
				away_scoreLast = away_score
				home_scoreLast = home_score
				print(home_score, away_score)

				time.sleep(1.5) # request every x seconds
				# END WHILE TRUE LOOP #

		elif game_status == "Final":
			if away:
				if away_score > home_score:
					time.sleep(stream_delay)
					win(abr) # PLAY GLORIA!
				else:
					print("Sorry for your loss.")
			elif home:
				if home_score > away_score:
					time.sleep(stream_delay)
					win(abr)
				else:
					print("Sorry for your loss.")
			else:
				print("Today's game is over.")
			
			break

		else: 
			print("Error involving game_status. Please try again.")

	else:
		print(f"That sucks, {abr} does not play today.")

	
if __name__ == "__main__":
	
	game = Config()
	team = Team(game.team_id)

	watch_game()