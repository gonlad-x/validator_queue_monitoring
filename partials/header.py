def header(last_updated):
  return f"""
    <div class="container py-3 my-2 text-center">
    	<h1 class="display-5 fw-bold text-capitalize mt-2">Ethereum Validator Queue</h1>
    	<div class="col-md-10 col-lg-6 mx-auto lead mb-3 opacity-75">
    		<small class="d-block fs-6">
    			Data provided by 
    			<a href="https://beaconcha.in/" target="_blank">beaconcha.in</a>
    		</small>
    		<small id="lastUpdated" class="d-block fst-italic fs-6" data-last-updated="{last_updated}"></small>
    	</div>
    </div>
  """
