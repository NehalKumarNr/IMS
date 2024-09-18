// Copyright (c) 2024, Nehal Kumar and contributors
// For license information, please see license.txt

frappe.ui.form.on('IMS Item Price', {
	setup(frm) {
		frm.set_query("item_code", function() {
			return {
				filters: {
					"disabled": 0
				}
			};
		});
	}
});
