import requests
import json


class Config:

	base_url = "https://statsapi.web.nhl.com/api/v1/"

	def __init__(self, abr):
		self.abr = abr


	def test(self):
		test = ''
		while test == '':
			testing = input("Run in test mode?(Y/N) ").upper()
			
			if testing == "Y":
				test = True # set to True to test with local json files
			elif testing == "N":
				test = False
			else:
				print("Please enter a valid test input.")

		return test


	def get_team(self, abr):
		r = requests.get(Config.base_url + "teams")
		data = r.json()

		for team in data['teams']:
			if team['abbreviation'] == abr:
				team_id = team['id']

		return team_id


	def stream_delay(self, test):
		if test:
			stream_delay = 0
		else:
			stream_delay = 34

		return stream_delay


	def data(self, test):
		if test:
			with open('sched.json') as f: # data from file for testing purposes
				data = json.load(f)
		else:
			r = requests.get(base_url + f"schedule?teamId={team_id}")
			data = r.json()

		return data