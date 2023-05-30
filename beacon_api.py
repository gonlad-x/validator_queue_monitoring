import requests
import os

def estimate_entry_waiting_time():
    response = requests.get('https://beaconcha.in/api/v1/validators/queue')
    data = response.json()
    beacon_entering = data["data"]["beaconchain_entering"]
    active_validators = data["data"]["validatorscount"]

    churn_limit = max(4, active_validators // 65536)
    activation_rate_per_epoch = churn_limit  # 4 validators per epoch (every 6.4 minutes) as a minimum

    waiting_time_epochs = beacon_entering / activation_rate_per_epoch
    waiting_time_seconds = waiting_time_epochs * 12 * 32  # 12 seconds per slot, 32 slots per epoch

    waiting_time_days = round(waiting_time_seconds // (24 * 3600))
    remaining_seconds = waiting_time_seconds % (24 * 3600)
    waiting_time_hours = round(remaining_seconds // 3600)
    remaining_seconds = remaining_seconds % 3600
    waiting_time_minutes = round(remaining_seconds // 60)

    return waiting_time_days, waiting_time_hours, waiting_time_minutes, waiting_time_seconds, beacon_entering, active_validators
def estimate_exit_waiting_time():
    validator_queue_url = "https://beaconcha.in/api/v1/validators/queue"
    validator_queue_data = requests.get(validator_queue_url).json()
    beacon_exiting = validator_queue_data["data"]["beaconchain_exiting"]
    active_validators = validator_queue_data["data"]["validatorscount"]

    churn_limit = max(4, active_validators // 65536)

    waiting_time_epochs = beacon_exiting / churn_limit
    waiting_time_seconds = waiting_time_epochs * 12 * 32  # 12 seconds per slot, 32 slots per epoch

    waiting_time_days = round(waiting_time_seconds // (24 * 3600))
    remaining_seconds = waiting_time_seconds % (24 * 3600)
    waiting_time_hours = round(remaining_seconds // 3600)
    remaining_seconds = remaining_seconds % 3600
    waiting_time_minutes = round(remaining_seconds // 60)

    return waiting_time_days, waiting_time_hours, waiting_time_minutes, waiting_time_seconds, beacon_exiting, active_validators

def format_value_and_units(value, units):
    # Pluralization of day, hour, and minute all simply add "s" to the end 
    return str(value) + " " + (units if value == 1 else units + 's')

def format_list_for_display(strings):
    print(strings)
    if not strings:
        return ""
    elif len(strings) == 1:
        # E.g. ["a"] -> "a"
        return strings[0]
    elif len(strings) == 2:
        # E.g. ["a", "b"] -> "a and b"
        return strings[0] + " and " + strings[1]
    else:
        # E.g. ["a", "b", "c"] -> "a, b, and c"
        formatted_string = ", ".join(strings[:-1])
        formatted_string += ", and " + strings[-1]
        return formatted_string

def generate_duration_label(days, hours, minutes):
    formatted_parts = []

    if days > 0:
        formatted_parts += [format_value_and_units(days, "day")]
    if hours > 0:
        formatted_parts += [format_value_and_units(hours, "hour")]
    if minutes > 0:
        formatted_parts += [format_value_and_units(minutes, "minute")]
    
    if len(formatted_parts) == 0:
        return "0 minutes"
    else:
        return format_list_for_display(formatted_parts)

def generate_html(entry_waiting_time_days, entry_waiting_time_hours, entry_waiting_time_minutes, beacon_entering, exit_waiting_time_days, exit_waiting_time_hours, exit_waiting_time_minutes, beacon_exiting, active_validators):
    entry_waiting_time = generate_duration_label(entry_waiting_time_days, entry_waiting_time_hours, entry_waiting_time_minutes)
    exit_waiting_time = generate_duration_label(exit_waiting_time_days, exit_waiting_time_hours, exit_waiting_time_minutes)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Validator Queue</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            background-color: #f4f4f4;
            padding: 1rem;
        }}

        h1 {{
            color: #333;
            font-size: 2rem;
        }}

        p {{
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 1.5rem;
        }}
    </style>
</head>
<body>
    <h1>Ethereum 2.0 Validator Queue</h1>
    <p>Estimated waiting time for new validators: {entry_waiting_time}</p>
    <p>Pending validators (entry queue): {beacon_entering}</p>
    <p>Estimated waiting time for exit queue: {exit_waiting_time}</p>
    <p>Pending validators (exit queue): {beacon_exiting}</p>
    <p>Active validators: {active_validators}</p>
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(html_content)

entry_waiting_time_days, entry_waiting_time_hours, entry_waiting_time_minutes, entry_waiting_time_seconds, beacon_entering, active_validators = estimate_entry_waiting_time()
exit_waiting_time_days, exit_waiting_time_hours, exit_waiting_time_minutes, exit_waiting_time_seconds, beacon_exiting, active_validators = estimate_exit_waiting_time()

generate_html(entry_waiting_time_days, entry_waiting_time_hours, entry_waiting_time_minutes, beacon_entering, exit_waiting_time_days, exit_waiting_time_hours, exit_waiting_time_minutes, beacon_exiting, active_validators)
