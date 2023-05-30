def queue_overview(entry_waiting_time, beacon_entering, exit_waiting_time, beacon_exiting):
	return f"""
		<div class="row row-cols-1 row-cols-md-2 gap-4 justify-content-center mx-1">

			<div class="card shadow border-light" style="max-width: 18rem;">
			  <div class="card-body">
			    <h5 class="card-title">Entry Queue</h5>
			    <p class="card-text">
			    	<div class="d-flex justify-content-between">
				    	<span>Validators: </span>
				    	<span>{"{:,}".format(beacon_entering)}</span>
			    	</div>
				    <div class="d-flex justify-content-between">
				    	<span>Wait: </span>
				    	<span>{entry_waiting_time}</span>
			    	</div>
				</p>
			  </div>
			</div>

			<div class="card shadow border-light" style="max-width: 18rem;">
			  <div class="card-body">
			    <h5 class="card-title">Exit Queue</h5>
			    <p class="card-text">
			    	<div class="d-flex justify-content-between">
			    		<span>Validators: </span>
			    		<span>{"{:,}".format(beacon_exiting)}</span>
		    		</div>
				    <div class="d-flex justify-content-between">
				    	<span>Wait: </span>
				    	<span>{exit_waiting_time}</span>
			    	</div>
				</p>
			  </div>
			</div>

		</div>
	"""
