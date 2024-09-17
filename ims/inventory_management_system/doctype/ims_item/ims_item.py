# Copyright (c) 2024, Nehal Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class IMSItem(Document):
    def autoname(self):
        self.item_code = make_autoname(self.item_group.upper()[:4] +'.-.####')
        self.name = self.item_code

    def after_insert(self):
        if self.standard_rate:
            self.item_price_list_created()

    def item_price_list_created(self):
        price_list = frappe.db.get_single_value('IMS Setting', 'price_list')
        if price_list:
            item_price = frappe.get_doc(
                {
                    "doctype": "IMS Item Price",
                    "price_list": price_list,
                    "item_code": self.name,
                    "uom": self.uom,
                    "rate": self.standard_rate,
                }
            )
            item_price.insert()
        else:
            frappe.throw("Select Price list in IMS setting")