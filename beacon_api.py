import requests
import json

BASE_URL = "https://beaconcha.in/api/v1"

def get_validator_queue():
    response = requests.get(f"{BASE_URL}/validators/queue")
    data = response.json()
    return data

def estimate_waiting_time():
    validator_queue = get_validator_queue()
    pending_validators = validator_queue["data"]["beaconchain_entering"]
    active_validators = validator_queue["data"]["validatorscount"]
    activation_rate = 4
    epoch_length_minutes = 6.4

    queue_epochs = pending_validators / activation_rate
    queue_time_minutes = queue_epochs * epoch_length_minutes

    hours = int(queue_time_minutes // 60)
    minutes = int(queue_time_minutes % 60)

    print(f"Number of active validators: {active_validators}")
    print(f"Number of pending validators: {pending_validators}")
    print(f"Estimated waiting time before a new validator is activated: {hours} hours {minutes} minutes")

if __name__ == "__main__":
    estimate_waiting_time()

