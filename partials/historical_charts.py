historical_charts = f"""
	<div class="row row-cols-1 justify-content-center mx-1">

		<div class="card shadow border-light mt-4">
		  <div class="card-body">
		    <h5 class="card-title">Validator Queue</h5>
		    <p class="card-text">
		    	<div>
					<canvas id="queueChart"></canvas>
				</div>
			</p>
		  </div>
		</div>

		<div class="card shadow border-light mt-4">
		  <div class="card-body">
		    <h5 class="card-title">Queue Wait Time (days)</h5>
		    <p class="card-text">
		    	<div>
					<canvas id="waitChart"></canvas>
				</div>
			</p>
		  </div>
		</div>

		<div class="card shadow border-light mt-4">
		  <div class="card-body">
		    <h5 class="card-title">Active Validators</h5>
		    <p class="card-text">
		    	<div>
					<canvas id="validatorChart"></canvas>
				</div>
			</p>
		  </div>
		</div>

		<div class="card shadow border-light mt-4">
		  <div class="card-body">
		    <h5 class="card-title">Supply Staked</h5>
		    <p class="card-text">
		    	<div>
					<canvas id="stakedChart"></canvas>
				</div>
			</p>
		  </div>
		</div>

		<div class="card shadow border-light mt-4">
		  <div class="card-body">
		    <h5 class="card-title">Staking APR</h5>
		    <p class="card-text">
		    	<div>
					<canvas id="aprChart"></canvas>
				</div>
			</p>
		  </div>
		</div>

	</div>
"""
