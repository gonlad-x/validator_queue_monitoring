import requests
import os
import math
import time
from partials.head import head
from partials.dark_mode_toggle import dark_mode_toggle


endpoint = "https://beaconcha.in/api/v1/validators/queue"
data = requests.get(endpoint).json()["data"]
last_updated = time.time()


def estimate_entry_waiting_time():
	beacon_entering = data["beaconchain_entering"]
	active_validators = data["validatorscount"]

	churn_limit = max(4, active_validators // 65536)
	activation_rate_per_epoch = churn_limit  # 4 validators per epoch (every 6.4 minutes) as a minimum
	waiting_time_epochs = beacon_entering / activation_rate_per_epoch
	entry_waiting_time = calculate_wait_time(waiting_time_epochs)

	return entry_waiting_time, beacon_entering, active_validators


def estimate_exit_waiting_time():
	beacon_exiting = data["beaconchain_exiting"]
	active_validators = data["validatorscount"]

	churn_limit = max(4, active_validators // 65536)
	waiting_time_epochs = beacon_exiting / churn_limit
	exit_waiting_time = calculate_wait_time(waiting_time_epochs)

	return exit_waiting_time, beacon_exiting, active_validators


def calculate_wait_time(waiting_time_epochs):
	waiting_time_seconds = waiting_time_epochs * 12 * 32  # 12 seconds per slot, 32 slots per epoch

	waiting_time_days = math.floor(waiting_time_seconds // 86400)
	waiting_time_days_hours = math.floor( (waiting_time_seconds % 86400)/86400*24 )
	waiting_time_hours = math.floor(waiting_time_seconds // 3600)
	waiting_time_hours_minutes = math.floor( (waiting_time_seconds % 3600)/3600*60 )


	if waiting_time_days > 0:
		days_text = "days"
		if waiting_time_days == 1:
			days_text = "day"
		hours_text = "hours"
		if waiting_time_days_hours == 1:
			hours_text = "hour"
		formatted_wait_time = f"""{waiting_time_days} {days_text}, {waiting_time_days_hours} {hours_text}"""
	else:
		hours_text = "days"
		if waiting_time_days == 1:
			hours_text = "day"
		minutes_text = "hours"
		if waiting_time_days_hours == 1:
			minutes_text = "hour"
		formatted_wait_time = f"""{waiting_time_hours} {hours_text}, {waiting_time_hours_minutes} {minutes_text}"""

	return formatted_wait_time


def generate_html(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, active_validators):
	html_content = f"""<!DOCTYPE html>
		<html lang="en">
		{head}
		<body>
			{dark_mode_toggle}

			<h1>Ethereum Validator Queue</h1>
			<p id="lastUpdated" data-last-updated="{last_updated}"></p>
			<p>Estimated waiting time for new validators: {entry_waiting_time}</p>
		    <p>Pending validators (entry queue): {"{:,}".format(beacon_entering)}</p>
		    <p>Estimated waiting time for exit queue: {exit_waiting_time}</p>
		    <p>Pending validators (exit queue): {"{:,}".format(beacon_exiting)}</p>
		    <p>Active validators: {"{:,}".format(active_validators)}</p>

			{footer}
		</body>
		</html>"""

	with open("index.html", "w") as f:
		f.write(html_content)

entry_waiting_time, beacon_entering, active_validators = estimate_entry_waiting_time()
exit_waiting_time, beacon_exiting, active_validators = estimate_exit_waiting_time()

generate_html(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, active_validators)
