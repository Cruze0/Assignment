frappe.pages['maintenance-dashboar'].on_page_load = function(wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Maintenance Dashboard',
		single_column: true
	});

	// Append dashboard HTML
	$(`
		<div class="dashboard-content p-4">
			<div class="row">
				<div class="col-md-6">
					<div class="card">
						<div class="card-body">
							<h4>Total Open Requests</h4>
							<h2 id="open-requests">Loading...</h2>
						</div>
					</div>
				</div>
				<div class="col-md-6">
					<div class="card">
						<div class="card-body">
							<h4>Total Critical Priority Requests</h4>
							<h2 id="critical-requests">Loading...</h2>
						</div>
					</div>
				</div>
			</div>

			<div class="row mt-4">
				<div class="col-md-12">
					<div class="card">
						<div class="card-body">
							<h4 class="card-title">Maintenance Requests by Status</h4>
							<div style="max-width: 300px; margin: auto;">
	<canvas id="status-chart"></canvas>
</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	`).appendTo(page.body);
	console.log("Dashboard HTML rendered");


	// Fetch and display total open requests
	frappe.db.count('Asset Maintenance Request', {
		filters: { status: 'Open' }
	}).then(count => {
		$('#open-requests').text(count);
	}).catch(() => {
		$('#open-requests').text("Error");
	});

	// Fetch and display total critical (urgent) requests
	frappe.db.count('Asset Maintenance Request', {
		filters: { priority: 'Urgent' }
	}).then(count => {
		$('#critical-requests').text(count);
	}).catch(() => {
		$('#critical-requests').text("Error");
	});

	// Load chart.js and render pie chart
	frappe.require("assets/frappe/node_modules/chart.js/dist/chart.umd.js", function () {
		console.log("Chart.js loaded");
		frappe.call({
			method: 'tech_task.technincal_task_assignment.dashboard.get_maintenance_status_summary',  // make sure spelling matches your module
			callback: function(r) {
				if (r.message && r.message.length > 0) {
					const data = r.message;
					const labels = data.map(row => row.status);
					const counts = data.map(row => row.count);

					new Chart(document.getElementById('status-chart'), {
						type: 'pie',
						data: {
							labels: labels,
							datasets: [{
								data: counts,
								backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
								hoverOffset: 10
							}]
						},
						options: {
							responsive: true,
							plugins: {
								legend: {
									position: 'bottom'
								},
								title: {
									display: true,
									text: 'Maintenance Requests by Status'
								}
							}
						}
					});
				} else {
					$('#status-chart').replaceWith('<p>No data to display.</p>');
				}
			}
		});
	});
};
