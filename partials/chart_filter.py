def chart_filter(chart):
	return f"""
		<div class="btn-group border mb-1" role="group" data-chart="{chart}" aria-label="Change chart timeframe">
			<input type="radio" class="btn-check" name="filter" id="{chart}filter-7" autocomplete="off">
			<label class="btn btn-outline-black btn-sm border px-sm-3" for="{chart}filter-7" onclick="updateData(this,7)">7d</label>

			<input type="radio" class="btn-check" name="filter" id="{chart}filter-30" autocomplete="off">
			<label class="btn btn-outline-black btn-sm border px-sm-3" for="{chart}filter-30" onclick="updateData(this,30)">30d</label>

			<input type="radio" class="btn-check" name="filter" id="{chart}filter-90" autocomplete="off">
			<label class="btn btn-outline-black btn-sm border px-sm-3" for="{chart}filter90" onclick="updateData(this,90)">90d</label>

			<input type="radio" class="btn-check" name="filter" id="{chart}filter-365" autocomplete="off">
			<label class="btn btn-outline-black btn-sm border px-sm-3" for="{chart}filter-365" onclick="updateData(this,365)">1y</label>

			<input type="radio" class="btn-check" name="filter" id="{chart}filter-0" autocomplete="off" checked>
			<label class="btn btn-outline-black btn-sm border px-sm-3 active" for="{chart}filter-0" onclick="updateData(this,0)">All</label>
		</div>
	"""
