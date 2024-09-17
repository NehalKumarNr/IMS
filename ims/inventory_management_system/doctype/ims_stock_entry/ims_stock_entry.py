# Copyright (c) 2024, Nehal Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class IMSStockEntry(Document):
	def before_save(self):
		total_amount = 0
		total_qty = 0
		for item in self.items:
			total_amount += flt(item.total_amount)
			total_qty += flt(item.qty) 
		self.total_amount = total_amount
		self.qty = total_qty

	def validate(self):
		self.validate_duplicate_data()

	def validate_duplicate_data(self):
		items_table = self.get('items')
		index = 1
		if self.stock_entry_type=="Material Transfer":
			for record in items_table:
				s_warehouse = record.source_warehouse
				t_warehouse = record.target_warehouse
				if s_warehouse == t_warehouse:
					frappe.throw("<b>Source Warehouse</b> & <b>Target Warehouse</b> in row no. {0} can not be same.".format(index))
				index = index + 1
		if self.stock_entry_type=="Material Issue":
			for record in items_table:
				if record.source_warehouse:
					frappe.throw("The <b>Source Warehouse</b> field must be left blank when performing a Material Issue.")

