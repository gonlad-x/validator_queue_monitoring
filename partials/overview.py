def overview(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting, current_churn, active_validators, amount_eth_staked, percent_eth_staked, staking_apr):
	return f"""
		<div class="row row-cols-1 row-cols-md-2 gap-4 justify-content-center mx-1">

			<div class="card shadow border-light" style="max-width: 18rem;">
			  <div class="card-body">
			    <h5 class="card-title">Entry Queue</h5>
			    <div class="card-text">
			    	<div class="d-flex justify-content-between">
				    	<span>Validators: </span>
				    	<span>{"{:,}".format(beacon_entering)}</span>
			    	</div>
				    <div class="d-flex justify-content-between">
				    	<span>Wait: </span>
				    	<span>{entry_waiting_time}</span>
			    	</div>
			    	<div class="d-flex justify-content-between">
				    	<span>Churn: </span>
				    	<span>{current_churn}/epoch</span>
			    	</div>
				</div>
			  </div>
			</div>

			<div class="card shadow border-light" style="max-width: 18rem;">
			  <div class="card-body">
			    <h5 class="card-title">Exit Queue</h5>
			    <div class="card-text">
			    	<div class="d-flex justify-content-between">
			    		<span>Validators: </span>
			    		<span>{"{:,}".format(beacon_exiting)}</span>
		    		</div>
				    <div class="d-flex justify-content-between">
				    	<span>Wait: </span>
				    	<span>{exit_waiting_time}</span>
			    	</div>
			    	<div class="d-flex justify-content-between">
				    	<span>Churn: </span>
				    	<span>{current_churn}/epoch</span>
			    	</div>
				</div>
			  </div>
			</div>

			<div class="card shadow border-light" style="max-width: 18rem;">
			  <div class="card-body">
			    <h5 class="card-title">Network</h5>
			    <div class="card-text">
			    	<div class="d-flex justify-content-between">
			    		<span>Active Validators: </span>
			    		<span>{"{:,}".format(active_validators)}</span>
		    		</div>
				    <div class="d-flex justify-content-between">
				    	<span>Staked ETH: </span>
				    	<span>{"{:,}".format(round(amount_eth_staked/100000)/10)}M ({percent_eth_staked}%)</span>
			    	</div>
			    	<div class="d-flex justify-content-between">
				    	<span>APR: </span>
				    	<span>{staking_apr}%</span>
			    	</div>
				</div>
			  </div>
			</div>

		</div>
	"""
