import requests
import os

def estimate_waiting_time():
    response = requests.get('https://beaconcha.in/api/v1/validators/queue')
    data = response.json()
    pending_validators = data["data"]["beaconchain_entering"]
    active_validators = data["data"]["validatorscount"]
    activation_rate = 4  # 4 validators per epoch (every 6.4 minutes)

    waiting_time_minutes = (pending_validators / activation_rate) * 6.4
    waiting_time_hours = waiting_time_minutes // 60
    waiting_time_minutes = round(waiting_time_minutes % 60)

    return waiting_time_hours, waiting_time_minutes, pending_validators, active_validators

def generate_html(waiting_time_hours, waiting_time_minutes, pending_validators, active_validators):
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
    <p>Estimated waiting time for new validators: {waiting_time_hours} hours and {waiting_time_minutes} minutes</p>
    <p>Pending validators: {pending_validators}</p>
    <p>Active validators: {active_validators}</p>
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(html_content)


waiting_time_hours, waiting_time_minutes, pending_validators, active_validators = estimate_waiting_time()
generate_html(waiting_time_hours, waiting_time_minutes, pending_validators, active_validators)
