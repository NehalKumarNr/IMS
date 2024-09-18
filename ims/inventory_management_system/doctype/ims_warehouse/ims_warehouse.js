// Copyright (c) 2024, Nehal Kumar and contributors
// For license information, please see license.txt

frappe.ui.form.on('IMS Warehouse', {
	setup(frm) {
		frm.set_query("parent_ims_warehouse", function() {
			return {
				filters: {
					"is_group": 1
				}
			};
		});
	}
});
