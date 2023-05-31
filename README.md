# Validator activation and exit times
Provide an estimate of the waiting time before your ETH 2 validator becomes active or elligible for exit.
The data is fetched using [this endpoint from beaconcha.in API](https://beaconcha.in/api/v1/docs/index.html#/Validator/get_api_v1_validators_queue). 

This is a fork of [gonlad-x's validator_queue_monitoring repo](https://github.com/gonlad-x/validator_queue_monitoring).

Create virtual environment
```
python -m venv validator_queue_monitoring
```

Enter virtual environment
```
validator_queue_monitoring\Scripts\activate
```

Install dependencies
```
python3 -m pip install urllib3==1.26.6
python3 -m pip install urllib3==1.26.6
```