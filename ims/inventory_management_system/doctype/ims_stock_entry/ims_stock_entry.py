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


