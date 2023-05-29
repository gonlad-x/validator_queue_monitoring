import requests
import os
import math
import time


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
	html_style = r"""
		body {
			font-family: Arial, sans-serif;
			max-width: 800px;
			margin: 0 auto;
			background-color: #f4f4f4;
			padding: 1rem;
		}
		.dark-mode body {
			background-color: #212529;
			color: #adb5bd;
		}

		h1 {
			color: #333;
			font-size: 2rem;
		}
		.dark-mode h1 {
			color: #adb5bd;
		}

		p {
			font-size: 1.1rem;
			color: #666;
			margin-bottom: 1.5rem;
		}
		.dark-mode p {
			color: #adb5bd;
		}

		.github-link {
			fill: #333;
		}
		.dark-mode .github-link {
			fill:  #c9d1d9;
		}

		#darkModeToggle {
			position: absolute;
			padding: 5px;
			cursor: pointer;
			right: 1rem;
			top: 0.5rem;
		}
		#darkModeToggle svg {
			height: 1.5rem;
			width: 1.5rem;
		}
		.d-none {
			display: none;
		}"""
	html_js = r"""
		checkDarkMode();
		lastUpdateTime();

		// Check if dark mode is set
		function checkDarkMode() {
			// Use past setting if available
			let darkModeEnabled = localStorage.getItem("darkModeEnabled");
			if (darkModeEnabled === null) {
				// Default to user browser theme preference
				let matched = window.matchMedia("(prefers-color-scheme: dark)").matches;
				if (matched) {
					setDarkMode("true");
				} else {
					setDarkMode("false");
				}
			} else {
				setDarkMode(darkModeEnabled);
			}
		}

		// Toggle dark mode theme
		function setDarkMode(enable) {
			document.getElementById("enableDarkMode").classList.add("d-none");
			document.getElementById("disableDarkMode").classList.add("d-none");
			var root = document.getElementsByTagName("html")[0];
			if (enable == "true") {
				// Enable dark mode
				root.classList.add("dark-mode");
				document.getElementById("disableDarkMode").classList.remove("d-none");
				localStorage.setItem("darkModeEnabled", "true");
			} else if (enable == "false") {
				// Disable dark mode
				root.classList.remove("dark-mode");
				document.getElementById("enableDarkMode").classList.remove("d-none");
				localStorage.setItem("darkModeEnabled", "false");
			}
		}

		function lastUpdateTime() {
			let lastUpdated = document.getElementById("lastUpdated");
			let currentEpoch = Math.floor( Date.now() / 1000);
			let updateEpoch = lastUpdated.getAttribute('data-last-updated');
			let timeSinceUpdate = Math.floor( (currentEpoch - updateEpoch)/60 );
			let lastUpdatedText = "Last updated: ";
			if (timeSinceUpdate > 0) {
				if (timeSinceUpdate > 1) {
					lastUpdatedText += `${timeSinceUpdate} minutes ago`;
				} else {
					lastUpdatedText += `${timeSinceUpdate} minute ago`;
				}
			} else {
				let timeSinceUpdate = Math.floor(currentEpoch - updateEpoch);
				if (timeSinceUpdate > 1) {
					lastUpdatedText += `${timeSinceUpdate} seconds ago`;
				} else {
					lastUpdatedText += `${timeSinceUpdate} second ago`;
				}
			}
			lastUpdated.innerHTML = lastUpdatedText;
		}
		"""
	html_content = f"""<!DOCTYPE html>
		<html lang="en">
		<head>
			<meta charset="UTF-8">
			<meta http-equiv="X-UA-Compatible" content="IE=edge">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Validator Queue</title>
			<style>
				{html_style}
			</style>
		</head>
		<body>
			<h1>Ethereum Validator Queue</h1>
			<p id="lastUpdated" data-last-updated="{last_updated}"></p>
			<p>Estimated waiting time for new validators: {entry_waiting_time}</p>
		    <p>Pending validators (entry queue): {"{:,}".format(beacon_entering)}</p>
		    <p>Estimated waiting time for exit queue: {exit_waiting_time}</p>
		    <p>Pending validators (exit queue): {"{:,}".format(beacon_exiting)}</p>
		    <p>Active validators: {"{:,}".format(active_validators)}</p>
			<hr>
			<p>
				<a href="https://github.com/etheralpha/validatorqueue-com" target="_blank">
					<svg height="40" width="40" aria-hidden="true" viewBox="0 0 16 16" version="1.1" data-view-component="true" class="github-link"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
				</a>
			</p>

			<div id="darkModeToggle">
				<span id="enableDarkMode" onclick="setDarkMode('true')">
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-brightness-high" viewBox="0 0 16 16">
						<path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
					</svg>
				</span>
				<span id="disableDarkMode" class="d-none" onclick="setDarkMode('false')">
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-brightness-high" viewBox="0 0 16 16">
						<path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
					</svg>
				</span>
			</div>

			<script type="text/javascript">
				{html_js}
			</script>
		</body>
		</html>"""

	with open("index.html", "w") as f:
		f.write(html_content)

entry_waiting_time, beacon_entering, active_validators = estimate_entry_waiting_time()
exit_waiting_time, beacon_exiting, active_validators = estimate_exit_waiting_time()

generate_html(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, active_validators)
