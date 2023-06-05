import requests
import os
import math
import time
import json
from datetime import datetime, timezone
from partials.head import head
from partials.dark_mode_toggle import dark_mode_toggle
from partials.header import header
from partials.overview import overview
from partials.faq import faq
from partials.historical_charts import historical_charts
from partials.footer import footer


queue_endpoint = "https://beaconcha.in/api/v1/validators/queue"
queue_data = requests.get(queue_endpoint).json()["data"]
epoch_endpoint = "https://mainnet.beaconcha.in/api/v1/epoch/finalized"
epoch_data = requests.get(epoch_endpoint).json()["data"]
apr_endpoint = "https://beaconcha.in/api/v1/ethstore/latest"
apr_data = requests.get(apr_endpoint).json()["data"]
supply_endpoint = "https://ultrasound.money/api/v2/fees/supply-over-time"
supply_data = requests.get(supply_endpoint).json()

last_updated = time.time()


def estimate_entry_waiting_time():
	beacon_entering = queue_data["beaconchain_entering"]
	active_validators = queue_data["validatorscount"]
	churn_limit = max(4, active_validators // 65536)

	entry_waiting_time, entry_waiting_time_days, current_churn, entry_churn, entry_churn_time_days = calculate_wait_time(active_validators, beacon_entering)

	return entry_waiting_time, entry_waiting_time_days, beacon_entering, active_validators, current_churn, entry_churn


def estimate_exit_waiting_time():
	beacon_exiting = queue_data["beaconchain_exiting"]
	active_validators = queue_data["validatorscount"]
	churn_limit = max(4, active_validators // 65536)

	exit_waiting_time, exit_waiting_time_days, current_churn, exit_churn, exit_churn_time_days = calculate_wait_time(active_validators, beacon_exiting)

	return exit_waiting_time, exit_waiting_time_days, beacon_exiting, exit_churn


def network_data():
	eth_supply = round(supply_data["d1"][0]["supply"])
	print("\neth_supply: \n\t" + str(eth_supply))
	amount_eth_staked = round(epoch_data["votedether"]/1000000000)
	print("\namount_eth_staked: \n\t" + str(amount_eth_staked))
	percent_eth_staked = round(amount_eth_staked/eth_supply * 10000)/100
	print("\npercent_eth_staked: \n\t" + str(percent_eth_staked))
	staking_apr = round(apr_data["avgapr7d"] * 10000)/100
	print("\nstaking_apr: \n\t" + str(staking_apr))

	return eth_supply, amount_eth_staked, percent_eth_staked, staking_apr


def calculate_wait_time(active_validators, queue):
	# different active validator levels and corresponding churn
	scaling = [0,327680,393216,458752,524288,589824,    655360,720896,786432,851968,917504,983040,1048576,1114112,1179648,1245184,1310720,1376256,1441792,1507328,1572864,1638400,1703936,1769472,1835008,1900544,1966080,2031616,2097152,2162688,2228224,2293760,2359296,2424832,2490368,2555904,2621440,2686976,2752512]
	epoch_churn = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]
	day_churn = [1000,1125,1350,1575,1800,2025,2250,2475,2700,2925,3150,3375,3600,3825,4050,4275,4500,4725,4950,5175,5400,5625,5850,6075,6300,6525,6750,6975,7200,7425,7650,7875,8100,8325,8550,8775,9000,9225,9450]
	current_churn = 9
	churn_time_days = 0
	churn_factor = 0
	
	for i, item in enumerate(scaling):
		if active_validators > scaling[i]:
			current_churn = epoch_churn[i]
		if (active_validators >= scaling[i]) and (active_validators < scaling[i+1]):
			j = i
			queue_remaining = queue
			while queue_remaining > 0:
				# different calcs for first run to account for starting in the middle of a level
				if (i == j):
					# if the entire queue empties in the current level
					if (active_validators + queue_remaining) < scaling[j+1]:
						churn_time_days += queue_remaining / day_churn[j]
						churn_factor += queue_remaining * epoch_churn[j]
						queue_remaining = 0
					# if the queue carries over into the next level
					else:
						churn_time_days += (scaling[j+1] - active_validators) / day_churn[j]
						churn_factor += (scaling[j+1] - active_validators) * epoch_churn[j]
						queue_remaining -= (scaling[j+1] - active_validators)
				# if the entire queue empties in the current level
				elif (scaling[j] + queue_remaining) < scaling[j+1]:
					churn_time_days += queue_remaining / day_churn[j]
					churn_factor += queue_remaining * epoch_churn[j]
					queue_remaining = 0
				# if the queue carries over into the next level
				else:
					churn_time_days += (scaling[j+1] - scaling[j]) / day_churn[j]
					churn_factor += (scaling[j+1] - scaling[j]) * epoch_churn[j]
					queue_remaining -= (scaling[j+1] - scaling[j])

				j += 1

	if (queue > 0):
		ave_churn = round(churn_factor / queue * 100) / 100
	else:
		ave_churn = current_churn

	print("\nchurn_time_days: \n\t" + str(churn_time_days))
	print("\ncurrent_churn: \n\t" + str(current_churn))
	print("\nave_churn: \n\t" + str(ave_churn))


	waiting_time_seconds = round(churn_time_days * 86400)

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


	return formatted_wait_time, waiting_time_days_raw, current_churn, ave_churn, churn_time_days


def update_historical_data():
	with open('historical_data.json', 'r') as f:
		all_data = json.load(f)
		date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
		todays_data =  {
			"date":date,
			"validators":active_validators,
			"entry_queue":beacon_entering,
			"entry_wait":round(entry_waiting_time_days*100)/100,
			"exit_queue":beacon_exiting,
			"exit_wait":round(exit_waiting_time_days*100)/100,
			"churn":current_churn,
			"entry_churn":entry_churn,
			"exit_churn":exit_churn,
			"supply":eth_supply,
			"staked_amount":amount_eth_staked,
			"staked_percent":percent_eth_staked,
			"apr":staking_apr
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
					

def generate_html(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, active_validators, current_churn, amount_eth_staked, percent_eth_staked, staking_apr, historical_data):
	html_content = f"""<!DOCTYPE html>
		<html lang="en">
		{head}
		<body>
			{dark_mode_toggle}
			<div class="container">
				{header(last_updated)}
				{overview(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, current_churn, active_validators, amount_eth_staked, percent_eth_staked, staking_apr)}
				{faq}
				{historical_charts}
				{footer(historical_data)}
			</div>
		</body>
		</html>"""

	with open("public/index.html", "w") as f:
		f.write(html_content)


entry_waiting_time, entry_waiting_time_days, beacon_entering, active_validators, current_churn, entry_churn = estimate_entry_waiting_time()
exit_waiting_time, exit_waiting_time_days, beacon_exiting, exit_churn = estimate_exit_waiting_time()
eth_supply, amount_eth_staked, percent_eth_staked, staking_apr = network_data()
historical_data = update_historical_data()

generate_html(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, active_validators, current_churn, amount_eth_staked, percent_eth_staked, staking_apr, historical_data)
