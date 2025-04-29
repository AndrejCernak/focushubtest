frappe.pages['focushub_dashboard'].on_page_load = function(wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'FocusHub Dashboard',
		single_column: true
	});

	$(page.body).html(`
		<style>
			body[data-route="focushub_dashboard"] .container.page-body {
				padding: 0 !important;
				max-width: 100% !important;
			}
			.focushub-dashboard {
				display: flex;
				height: calc(100vh - 120px);
				width: 100%;
			}
			.focushub-sidebar {
				width: 220px;
				background: #ffffff;
				border-right: 1px solid #eee;
				display: flex;
				flex-direction: column;
				padding-top: 1rem;
			}
			.focushub-sidebar .nav-link {
				padding: 0.75rem 1rem;
				color: #333;
				font-size: 14px;
				display: flex;
				align-items: center;
				gap: 0.5rem;
				border-left: 3px solid transparent;
				text-decoration: none;
			}
			.focushub-sidebar .nav-link:hover {
				background: #f8f9fa;
			}
			.focushub-sidebar .nav-link.active {
				background: #f1f3f5;
				border-left: 3px solid #339af0;
				font-weight: 600;
			}
			.focushub-content {
				flex-grow: 1;
				padding: 2rem;
				overflow-y: auto;
			}
				/* Hide top nav bar and header */
header.navbar,
.page-head,
.page-title,
.breadcrumb-container {
	display: none !important;
}

/* Remove top padding that was reserved for the header */
body[data-route="focushub_dashboard"] .page-content {
	padding-top: 0 !important;
}

		</style>

		<div class="focushub-dashboard">
			<div class="focushub-sidebar">
				<a href="#" class="nav-link active" data-section="overview">📊 Overview</a>
				<a href="#" class="nav-link" data-section="clenovia">👥 Clenovia</a>
				<a href="#" class="nav-link" data-section="faktura_prijata">📥 Faktura Prijatá</a>
				<a href="#" class="nav-link" data-section="faktura_vystavena">📤 Faktura Vystavená</a>
				<a href="#" class="nav-link" data-section="vydavky">💸 Výdavky</a>
				<a href="#" class="nav-link" data-section="prijmy">💰 Príjmy</a>
			</div>
			<div class="focushub-content" id="focushub-content">
				<h4>Welcome to FocusHub</h4>
				<p>Select a section on the left to get started.</p>
			</div>
		</div>
	`);

	const contentMap = {
		overview: `<h4>Overview</h4><p>This is your dashboard overview.</p>`,
		clenovia: `<iframe src="/app/clenovia" style="width:100%; height:80vh; border:none;"></iframe>`,
		faktura_prijata: `<iframe src="/app/faktura-prijata" style="width:100%; height:80vh; border:none;"></iframe>`,
		faktura_vystavena: `<iframe src="/app/faktura-vystavena" style="width:100%; height:80vh; border:none;"></iframe>`,
		vydavky: `<iframe src="/app/vydavky" style="width:100%; height:80vh; border:none;"></iframe>`,
		prijmy: `<iframe src="/app/prijmy" style="width:100%; height:80vh; border:none;"></iframe>`
	};

	$('.focushub-sidebar .nav-link').on('click', function (e) {
		e.preventDefault();
		const section = $(this).data('section');

		$('.focushub-sidebar .nav-link').removeClass('active');
		$(this).addClass('active');

		$('#focushub-content').html(contentMap[section] || '<p>Section not found.</p>');
	});
};
