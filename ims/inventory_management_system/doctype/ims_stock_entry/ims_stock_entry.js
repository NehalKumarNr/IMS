// Copyright (c) 2024, Nehal Kumar and contributors
// For license information, please see license.txt

frappe.ui.form.on('IMS Stock Entry', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('IMS Stock Entry Detail', {
    qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
		let total_amount = (row.qty || 0) * (row.rate || 0);
		frappe.model.set_value(cdt, cdn, 'total_amount', total_amount);
    },
    rate: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
		let total_amount = (row.qty || 0) * (row.rate || 0);
		frappe.model.set_value(cdt, cdn, 'total_amount', total_amount);
    },
	item_code:function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		let total_amount = (row.qty || 0) * (row.rate || 0);
		frappe.model.set_value(cdt, cdn, 'total_amount', total_amount);
	}
});
