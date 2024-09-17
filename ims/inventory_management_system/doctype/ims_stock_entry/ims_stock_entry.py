# Copyright (c) 2024, Nehal Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _

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
        self.avoid_duplicate_entry_in_stock_level()

    def on_submit(self):
        self.update_ims_item_stock_level()
    
    def on_cancel(self):
        self.cancel_ims_item_stock_level()

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
                if not s_warehouse or not t_warehouse:
                    frappe.throw("<b>Source Warehouse</b> & <b>Target Warehouse</b> must not be empty")
        if self.stock_entry_type=="Material Issue":
            for record in items_table:
                if record.source_warehouse:
                    frappe.throw("The <b>Source Warehouse</b> field must be left blank when performing a Material Issue.")
                if not record.target_warehouse:
                    frappe.throw("The <b>Target Warehouse</b> field must not be empty.")

    def update_ims_item_stock_level(self):
        if self.stock_entry_type == "Material Issue":
            for item in self.items:
                item_doc = frappe.get_doc("IMS Item", item.item_code)
                
                warehouse_found = False
                for stock_level in item_doc.stock_level:
                    if stock_level.warehouse == item.target_warehouse:
                        stock_level.qty += item.qty
                        warehouse_found = True
                        break
                if not warehouse_found:
                    item_doc.append("stock_level", {
                        "warehouse": item.target_warehouse,
                        "qty": item.qty
                    })
                item_doc.save()
        if self.stock_entry_type == "Material Transfer":
            for item in self.items:
                item_doc = frappe.get_doc("IMS Item", item.item_code)
            source_warehouse_found = False
            for stock_level in item_doc.stock_level:
                if stock_level.warehouse == item.source_warehouse:
                    if stock_level.qty >= item.qty:
                        stock_level.qty -= item.qty
                    else:
                        frappe.throw(f"Not enough stock in source warehouse: {item.source_warehouse}")
                    source_warehouse_found = True
                    break
            if not source_warehouse_found:
                frappe.throw(f"Source warehouse: {item.source_warehouse} not found for item {item.item_code}")
            
            target_warehouse_found = False
            for stock_level in item_doc.stock_level:
                if stock_level.warehouse == item.target_warehouse:
                    stock_level.qty += item.qty
                    target_warehouse_found = True
                    break
            if not target_warehouse_found:
                item_doc.append("stock_level", {
                    "warehouse": item.target_warehouse,
                    "qty": item.qty
                })
            item_doc.save()
    
    def cancel_ims_item_stock_level(self):
        if self.stock_entry_type == "Material Issue":
            for item in self.items:
                item_doc = frappe.get_doc("IMS Item", item.item_code)
                
                warehouse_found = False
                for stock_level in item_doc.stock_level:
                    if stock_level.warehouse == item.target_warehouse:
                        if stock_level.qty >= item.qty:
                            stock_level.qty -= item.qty
                        else:
                            frappe.throw(f"Not enough stock in target warehouse to cancel: {item.target_warehouse}")
                        warehouse_found = True
                        break
                if not warehouse_found:
                    frappe.throw(f"Target warehouse: {item.target_warehouse} not found for item {item.item_code}")
                
                item_doc.save()

        if self.stock_entry_type == "Material Transfer":
            for item in self.items:
                item_doc = frappe.get_doc("IMS Item", item.item_code)

                target_warehouse_found = False
                for stock_level in item_doc.stock_level:
                    if stock_level.warehouse == item.target_warehouse:
                        if stock_level.qty >= item.qty:
                            stock_level.qty -= item.qty
                        else:
                            frappe.throw(f"Not enough stock in target warehouse: {item.target_warehouse} to cancel transfer")
                        target_warehouse_found = True
                        break
                if not target_warehouse_found:
                    frappe.throw(f"Target warehouse: {item.target_warehouse} not found for item {item.item_code}")

                source_warehouse_found = False
                for stock_level in item_doc.stock_level:
                    if stock_level.warehouse == item.source_warehouse:
                        stock_level.qty += item.qty
                        source_warehouse_found = True
                        break
                if not source_warehouse_found:
                    item_doc.append("stock_level", {
                        "warehouse": item.source_warehouse,
                        "qty": item.qty
                    })
                item_doc.save()

    
    def avoid_duplicate_entry_in_stock_level(self):
        item_code = set()
        for item in self.items:
            if item.item_code in item_code:
                frappe.throw(_("Found multiple entries for same <b>Item Code.</b>"))
            item_code.add(item.item_code)

