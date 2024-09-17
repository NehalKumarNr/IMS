# Copyright (c) 2024, Nehal Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import (
    cint,
    cstr,
    flt,
    formatdate,
    get_link_to_form,
    getdate,
    now_datetime,
    nowtime,
    strip,
    strip_html,
)

class IMSItem(Document):
    def autoname(self):
        self.item_code = make_autoname(self.item_group.upper()[:4] +'.-.####')
        self.name = self.item_code

    def after_insert(self):
        if self.standard_rate:
            self.item_price_list_created()
        if self.opening_stock:
            self.create_opening_stock()

    def item_price_list_created(self):
        price_list = frappe.db.get_single_value('IMS Setting', 'price_list')
        if self.disabled==0:
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

    def create_opening_stock(self):
        if not self.maintain_stock:
            return

        if not self.valuation_rate and not self.standard_rate:
            frappe.throw(_("Valuation Rate or Standard Rate is mandatory if Opening Stock entered"))

        if self.disabled==0:
            warehouse = frappe.db.get_single_value('IMS Setting', 'default_warehouse')
            if warehouse:
                stock_entry = frappe.get_doc({
                    "doctype": "IMS Stock Entry",
                    "stock_entry_type": "Material Issue",
                    "posting_date": getdate(),
                    "posting_time": nowtime(),
                    "items": [
                        {
                            "target_warehouse": warehouse,
                            "item_code": self.name,
                            "qty": self.opening_stock,
                            "rate": self.valuation_rate or self.standard_rate,
                            "total_amount": self.opening_stock * (self.valuation_rate or self.standard_rate)
                        }
                    ]
                })
                stock_entry.insert()
                stock_entry.submit()
            else:
                frappe.throw("Select Warehouse in IMS setting")
    