import requests
import os
import math
import time
import json
from datetime import datetime
from partials.head import head
from partials.dark_mode_toggle import dark_mode_toggle
from partials.header import header
from partials.queue_overview import queue_overview
from partials.historical_charts import historical_charts
from partials.footer import footer


endpoint = "https://beaconcha.in/api/v1/validators/queue"
data = requests.get(endpoint).json()["data"]
last_updated = time.time()


def estimate_entry_waiting_time():
	beacon_entering = data["beaconchain_entering"]
	active_validators = data["validatorscount"]

	churn_limit = max(4, active_validators // 65536)
	waiting_time_epochs = beacon_entering / churn_limit
	entry_waiting_time, entry_waiting_time_days = calculate_wait_time(waiting_time_epochs)

	return entry_waiting_time, entry_waiting_time_days, beacon_entering, active_validators


def estimate_exit_waiting_time():
	beacon_exiting = data["beaconchain_exiting"]
	active_validators = data["validatorscount"]

	churn_limit = max(4, active_validators // 65536)
	waiting_time_epochs = beacon_exiting / churn_limit
	exit_waiting_time, exit_waiting_time_days = calculate_wait_time(waiting_time_epochs)

	return exit_waiting_time, exit_waiting_time_days, beacon_exiting, active_validators


def calculate_wait_time(waiting_time_epochs):
	waiting_time_seconds = waiting_time_epochs * 12 * 32  # 12 seconds per slot, 32 slots per epoch

	waiting_time_months = math.floor(waiting_time_seconds // 2592000)
	waiting_time_months_days = round( (waiting_time_seconds % 2592000)/2592000*30 )

	waiting_time_days = math.floor(waiting_time_seconds // 86400)
	waiting_time_days_hours = round( (waiting_time_seconds % 86400)/86400*24 )

	waiting_time_hours = math.floor(waiting_time_seconds // 3600)
	waiting_time_hours_minutes = round( (waiting_time_seconds % 3600)/3600*60 )

	waiting_time_days_raw = waiting_time_seconds / 86400

	# if waiting_time_months > 0:
	#   months_text = "months"
	#   days_text = "days"
	#   if waiting_time_months == 1:
	#       months_text = "month"
	#   if waiting_time_months_days == 1:
	#       days_text = "day"
	#   formatted_wait_time = f"""{waiting_time_months} {months_text}, {waiting_time_months_days} {days_text}"""
	if waiting_time_days > 0:
		days_text = "days"
		hours_text = "hours"
		if waiting_time_days == 1:
			days_text = "day"
		if waiting_time_days_hours == 1:
			hours_text = "hour"
		formatted_wait_time = f"""{waiting_time_days} {days_text}, {waiting_time_days_hours} {hours_text}"""
	elif waiting_time_hours > 0:
		hours_text = "hours"
		minutes_text = "minutes"
		if waiting_time_hours == 1:
			hours_text = "hour"
		if waiting_time_hours_minutes == 1:
			minutes_text = "minute"
		formatted_wait_time = f"""{waiting_time_hours} {hours_text}, {waiting_time_hours_minutes} {minutes_text}"""
	else:
		minutes_text = "minutes"
		if waiting_time_hours_minutes == 1:
			minutes_text = "minute"
		formatted_wait_time = f"""{waiting_time_hours_minutes} {minutes_text}"""


	return formatted_wait_time, waiting_time_days_raw


def update_historical_data(entry_waiting_time_days, exit_waiting_time_days):
	with open('historical_data.json', 'r') as f:
		all_data = json.load(f)
		date = datetime.today().strftime('%Y-%m-%d')
		todays_data =  {
			"date":date,
			"validators":active_validators,
			"entry_queue":beacon_entering,
			"entry_wait":round(entry_waiting_time_days*100)/100,
			"exit_queue":beacon_exiting,
			"exit_wait":round(exit_waiting_time_days*100)/100
		}
		print("\nhistorical_data: \n\t" + str(all_data))
		print("\ntodays_data: \n\t" + str(todays_data))
		if len(all_data) > 0 and all_data[-1].get('date') is not None:
			if date != all_data[-1]['date']:
				all_data.append(todays_data)
				with open('historical_data.json', 'w') as f:
					json.dump(all_data, f, indent=None, separators=(',', ':'))
				f.close()
				print("historical data has been updated")
			else:
				print("historical data for the current date was already recorded")
		return all_data
					

def generate_html(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, active_validators, historical_data):
	html_content = f"""<!DOCTYPE html>
		<html lang="en">
		{head}
		<body>
			{dark_mode_toggle}
			<div class="container">
				{header(last_updated)}
				{queue_overview(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting)}
				{historical_charts}
				{footer(historical_data)}
			</div>
		</body>
		</html>"""

	with open("public/index.html", "w") as f:
		f.write(html_content)


entry_waiting_time, entry_waiting_time_days, beacon_entering, active_validators = estimate_entry_waiting_time()
exit_waiting_time, exit_waiting_time_days, beacon_exiting, active_validators = estimate_exit_waiting_time()
historical_data = update_historical_data(entry_waiting_time_days, exit_waiting_time_days)

generate_html(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, active_validators, historical_data)
