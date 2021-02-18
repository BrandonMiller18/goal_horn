import requests
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Config:

	base_url = "https://statsapi.web.nhl.com"

	def __init__(self):
		self.test()
		self.get_abr()
		self.get_team(self.abr)
		self.get_data(self.test, self.team_id)
		self.stream_delay(self.test)

	def test(self):

		testing = input("TESTING?\nY for yes\nEnter for no").upper()
		
		if testing == "Y":
			self.test = True # set to True to test with local json files
		else:
			self.test = False

		print("\n")


	def get_abr(self):
		self.abr = input("Please enter the abbreviation of your favorite team!\n").upper()
		print("\n")



	def get_team(self, abr):
		r = requests.get(self.base_url + "/api/v1/teams")
		data = r.json()
			
		for team in data['teams']:
			if team['abbreviation'] == abr:
				self.team_id = team['id']

		print(f"Team ID set to {self.team_id}...")


	def stream_delay(self, test):
		if test:
			self.stream_delay = 0
		else:
			self.stream_delay = 34

		print(f"Stream delay set to {self.stream_delay}...\n")


	def get_data(self, test, team_id):
		if test:
			with open('sched.json') as f: # data from file for testing purposes
				self.data = json.load(f)
		else:
			r = requests.get(self.base_url + f"/api/v1/schedule?teamId={team_id}&expand=schedule.linescore")
			self.data = r.json()

		return self.data




class Team:

	base_url = "https://statsapi.web.nhl.com"

	def __init__(self, team_id):
		self.team_id = team_id
		self.get_team_info(self.team_id)
		self.get_team_players(self.team_id)

	def get_team_info(self, team_id):
		r = requests.get(self.base_url + f"/api/v1/teams/{team_id}")
		data = r.json()

		self.team_name = data['teams'][0]['name']
		self.team_short_name = data['teams'][0]['franchise']['teamName']
		self.city = data['teams'][0]['venue']['city']
		self.venue = data['teams'][0]['venue']['name']

		self.team_info = {
			"teamName": self.team_name,
			"nickname": self.team_short_name,
			"city": self.city,
			"venue": self.venue,
			}


	def get_team_players(self, team_id):
		r = requests.get(self.base_url + f"/api/v1/teams/{team_id}/roster")
		data = r.json()
		self.roster = data['roster']

		numbers = []
		names = []

		x = 0

		for p in self.roster:
			p = self.roster[x]['jerseyNumber']
			numbers.append(p)

			p = self.roster[x]['person']['fullName']
			names.append(p)

			x += 1

		self.players = dict(zip(numbers, names))
