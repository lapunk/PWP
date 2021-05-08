import json, requests
from termcolor import colored


API_URL = "http://127.0.0.1:5000/api"
GREEN_LINE = colored("---------------------------------------", 'green')
YELLOW_LINE = colored("---------------------------------------", 'yellow')

class Plant:
	def get_all_plants(self):
		print(YELLOW_LINE)
		print(colored("  All saved plants       ", 'white'))
		print(YELLOW_LINE)
		resp = requests.get(API_URL + "/plants/")
		try:
			body = resp.json()
		except ValueError:
			return print(colored("\nNO PLANTS SAVED\n", 'red'))
		print(GREEN_LINE)
		for item in body["items"]:
			print("Name: " + str(item["name"]))
			print(GREEN_LINE)
		print("\n")
		return

	def get_single_plant(self):
		print(YELLOW_LINE)
		print(colored("   Plant's information", 'yellow'))
		print(YELLOW_LINE)
		giv_input = input("Give plant's name: ")
		if not giv_input:
			print(colored("Name can't be null, try again\n", 'red'))
			return
		print("\n")
		resp = requests.get(API_URL + "/plants/{}/".format(giv_input))
		try:
			body = resp.json()
			print("{}'s info: ".format(body["name"]))
			print(GREEN_LINE)
			print("Specie: " + str(body["specie"]))
			print("Location: " + str(body["location"]))
		except (ValueError, KeyError):
			print(colored("No plant with name {} saved".format(giv_input), 'red'))
		print(GREEN_LINE)
		print("\n")

	def add_plant(self):
		print(YELLOW_LINE)
		print(colored("  Add new plant", 'yellow'))
		print(YELLOW_LINE)
		plant_data = {}
		input_name = input("Give plant's unique name: ")
		if not input_name:
			return print(colored("Name can't be null, try again\n", 'red'))
		plant_data["name"] = input_name

		input_specie = input("Give plant's specie: ")
		if not input_specie:
			return print(colored("Specie can't be null, try again\n", 'red'))
		plant_data["specie"] = input_specie

		input_location = input("Give plant's location (optional): ")
		plant_data["location"] = str(input_location)

		r = requests.post(API_URL + "/plants/", data=json.dumps(plant_data),
			headers={"Content-type": "application/json"})

		if r.status_code != 201:
			print("\nstatus : " + str(r.status_code))
			print(colored("Something went wrong, try again \n", 'red'))
		else:
			print(colored("\n!!New plant added!!\n", 'green'))
		return 

	def modify_plant(self):
		print(YELLOW_LINE)
		print(colored("  Modify saved plant", 'yellow'))
		print(YELLOW_LINE)   
		plant_data = {}

		name = input("Give name of plant to be modified: ")
		if not name:
			print(colored("Name can't be null\n", 'red'))
			return

		plant_data["name"] = name
		specie = input("Give new specie: ")
		if not specie:
			print(colored("Specie can't be null\n", 'red'))
			return
		plant_data["specie"] = specie

		location = input("Give new location (optional): ")
		plant_data["location"] = location

		r = requests.put(API_URL + "/plants/{}/".format(name), data=json.dumps(plant_data),
			headers={"Content-type": "application/json"})
		if r.status_code != 204:
			print("\nstatus : " + str(r.status_code))
			print(colored("Something went wrong, try again\n", 'red'))
			return
		print("\n")
		print(colored("!!Plant {} updated!!".format(name), 'green'))
		print("\n")
		return


	def delete_plant(self):
		print(YELLOW_LINE)
		print(colored("  Delete saved plant", 'yellow'))
		print(YELLOW_LINE)  
		name = input("Give name of the plant to be deleted: ")
		if not name:
			return print(colored("Name can't be null, try again", 'red'))
		r = requests.delete(API_URL + "/plants/{}/".format(name))
		if r.status_code != 204:
			print("\nStatus : " + str(r.status_code))
			return print(colored("Something went wrong, try again\n", 'red'))
		print(colored("\n!!Plant {} delete success!!\n".format(name), 'green'))

	def __init__(self):
		pass