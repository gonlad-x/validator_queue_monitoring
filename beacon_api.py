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
    beacon_entering = "{:,}".format(beacon_entering)
    beacon_exiting = "{:,}".format(beacon_exiting)
    active_validators = "{:,}".format(active_validators)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, user-scalable=no">
    <title>Ethereum Validator Queue Status</title>
    <style>
        html {{
            background-color: #f9f9f9;
        }}
        body {{
            font-family: system-ui, Helvetica, Arial, sans;
            margin: 0;
            padding: 0px;
            text-align: center;
            color: #6b68a6;
            padding: 20px;
            overflow-x: hidden;
        }}
        a {{
            color: #6b68a6;
        }}
        h1 {{
            text-align: center;
            margin: 10px 0 20px 0;
            padding: 0;
        }}
        h2 {{
            font-size: 20px;
            margin: 0 0 20px 0;
            padding: 0;
        }}
        .container {{
            display: flex;
            justify-content: center;
            flex-direction: column;
            align-items: center;
        }}
        .boxes {{
            display: flex;
            justify-content: center;
            gap: 10px;
        }}
        .box {{
            background-color: #e1d2fb;
            border: 2px solid #b5b2de;
            color: #6b68a6;
            padding: 20px;
            text-align: center;
            flex-shrink: 0;
            z-index: 2;
        }}
        .count {{
            font-size: 30px;
            text-align: center;
        }}
        .count-label {{
            margin-bottom: 1em;
        }}
        .time {{
            font-size: 18px;
        }}
        svg {{
            width: 500px;
            height: 180px;
            position: relative;
            top: 0px;
            z-index: 1;
            margin-bottom: 20px;
        }}
        @media screen and (max-width: 850px) {{
            .boxes {{
                flex-direction: column;
                align-items: center;
            }}
            .box {{
                width: 270px;
                color: #8e89f1;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Ethereum Validator Queue Status</h1>
        <div class="boxes">
            <div class="box">
                <h2>Pending Activations</h2>
                <div class="count">{beacon_entering}</div>
                <div class="count-label">validators</div>
                <div class="time-label">Estimated wait time:</div>
                <div class="time">{entry_waiting_time}</div>
            </div>
            <div class="box">
                <h2>Active validators</h2>
                <div class="count">{active_validators}</div>
                <div class="count-label">validators</div>
            </div>
            <div class="box">
                <h2>Pending Withdrawals</h2>
                <div class="count">{beacon_exiting}</div>
                <div class="count-label">validators</div>
                <div class="time-label">Estimated wait time:</div>
                <div class="time">{exit_waiting_time}</div>
            </div>
        </div>
        <svg>
            <linearGradient id="g1" x1="100%" y1="100%" x2="100%" y2="0%">
                <stop stop-color="#E1D2FB" stop-opacity="1" offset="0"/>
                <stop stop-color="#E1D2FB" stop-opacity="0" offset="0.75"/>
            </linearGradient>
            <linearGradient id="g2" x1="0%" y1="50%" x2="100%" y2="50%">
                <stop stop-color="#a7bfbd" offset="0"/>
                <stop stop-color="#4c7471" offset="0.5"/>
                <stop stop-color="#a7bfbd" offset="1"/>
            </linearGradient>
            <linearGradient id="g3" x1="100%" y1="100%" x2="100%" y2="0%">
                <stop stop-color="#ae92db" offset="0"/>
                <stop stop-color="#E1D2FB" offset="1"/>
            </linearGradient>
            <rect x="160" y="120" width="180" height="10" stroke="#4c7471" fill="url(#g2)" />
            <rect x="210" y="130" width="10" height="40" fill="#a7bfbd" />
            <rect x="280" y="130" width="10" height="40" fill="#a7bfbd" />
            <rect x="200" y="165" width="100" height="10" stroke="#4c7471" fill="#a7bfbd" />
            <rect x="220" y="170" width="60" height="8" stroke="#444" fill="#666" />
            <rect x="223" y="172" width="6" height="4" fill="#a3f5f9" />
            <path d="m -6 16 L -51 -18 a 100 100 0 0 1 101 0 l -44 34 z" fill="url(#g1)" transform="translate(250 100) scale(4)" />
            <polygon points="0 -40, 30 0, 0 40, -30 0" fill="url(#g3)" stroke="#9391b6" stroke-width="2" transform="translate(230 110) scale(0.25)"/>
            <polygon points="0 -60, 30 0, 0 90, -30 0" fill="url(#g3)" stroke="#9391b6" stroke-width="2" transform="translate(250 115) scale(0.35)"/>
            <polygon points="0 -40, 30 0, 0 40, -30 0" fill="url(#g3)" stroke="#9391b6" stroke-width="2" transform="translate(275 120) scale(0.25)"/>
            <polygon points="0 -40, 30 0, 0 40, -30 0" fill="url(#g3)" stroke="#9391b6" stroke-width="2" transform="translate(235 130) scale(0.2)"/>
            <polygon points="0 -40, 30 0, 0 40, -30 0" fill="url(#g3)" stroke="#9391b6" stroke-width="2" transform="translate(265 105) scale(0.2)"/>
        </svg>
        <footer>
            <p>Made with &#128156; for waiting in line (so long as I'm in it with you) by <a href="https://twitter.com/MikeSylphDapps" target="_blank" rel="noreferrer">mike.sylphdapps.eth</a>.</p>
            <p>Forked from gonlad-x's <a href="https://validator-queue-monitoring.vercel.app/" target="_blank" rel="noreferrer">validator-queue-monitoring</a>.</p>
            <p>You can see my other work at <a href="https://sylphdapps.com/" target="_blank" rel="noreferrer">Sylph Dapps</a>.</p>
        </footer>
    </div>
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(html_content)

entry_waiting_time_days, entry_waiting_time_hours, entry_waiting_time_minutes, entry_waiting_time_seconds, beacon_entering, active_validators = estimate_entry_waiting_time()
exit_waiting_time_days, exit_waiting_time_hours, exit_waiting_time_minutes, exit_waiting_time_seconds, beacon_exiting, active_validators = estimate_exit_waiting_time()

generate_html(entry_waiting_time_days, entry_waiting_time_hours, entry_waiting_time_minutes, beacon_entering, exit_waiting_time_days, exit_waiting_time_hours, exit_waiting_time_minutes, beacon_exiting, active_validators)
