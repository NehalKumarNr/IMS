// Copyright (c) 2024, Nehal Kumar and contributors
// For license information, please see license.txt

frappe.ui.form.on('IMS Item', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('IMS Item', "item_group", function(frm) {
	var group ="";
	group = cur_frm.doc.item_group.slice(0, 4).toUpperCase();
	frm.set_value("item_code",group);
	refresh_field("item_code");
});