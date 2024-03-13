# validatorqueque-com

This repo contains the source code for the [ValidatorQueue.com](https://validatorqueque.com).

Provides an estimate of the waiting time before your Ethereum validator becomes active or eligible for exit.
The data is fetched using the [beaconcha.in API](https://beaconcha.in/api/v1/docs/index.html#/Validator/get_api_v1_validators_queue).

The data is updated every ~ 15min. The first reading of each UTC+0 day is recorded for historical data.

To execute locally, run `python build.py`. If that doesn't work then try `python3 build.py`.

This project is maintained by [Ether Alpha](https://etheralpha.org/).
