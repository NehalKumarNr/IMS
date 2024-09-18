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
		frappe.call({
			method: 'ims.inventory_management_system.doctype.ims_stock_entry.ims_stock_entry.item_rate',
			args: {item_code: row.item_code},
			callback: function(r) {
				frappe.model.set_value(cdt, cdn, 'rate', r.message);
			}
		})

	}
});
