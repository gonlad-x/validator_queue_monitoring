historical_charts = f"""
	<div class="row row-cols-1 justify-content-center mx-1">

		<div class="card shadow border-light mt-4">
		  <div class="card-body">
		    <h5 class="card-title">Historical Validator Queue</h5>
		    <p class="card-text">
		    	<div>
					<canvas id="queueChart"></canvas>
				</div>
			</p>
		  </div>
		</div>

		<div class="card shadow border-light mt-4">
		  <div class="card-body">
		    <h5 class="card-title">Historical Wait Time (days)</h5>
		    <p class="card-text">
		    	<div>
					<canvas id="waitChart"></canvas>
				</div>
			</p>
		  </div>
		</div>

		<div class="card shadow border-light mt-4">
		  <div class="card-body">
		    <h5 class="card-title">Historical Validator Count</h5>
		    <p class="card-text">
		    	<div>
					<canvas id="validatorChart"></canvas>
				</div>
			</p>
		  </div>
		</div>

	</div>
"""
