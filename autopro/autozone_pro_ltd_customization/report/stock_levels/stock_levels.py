# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 140
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "item_group",
            "label": _("Item Group"),
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 140
        },
        {
            "fieldname": "stock_qty",
            "label": _("Stock Qty"),
            "fieldtype": "Float",
            "width": 110
        },
        {
            "fieldname": "stock_value",
            "label": _("Stock Value"),
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "fieldname": "valuation_rate",
            "label": _("Valuation Rate"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "slow_moving",
            "label": _("Slow Moving"),
            "fieldtype": "Check",
            "width": 100
        },
        {
            "fieldname": "disabled",
            "label": _("Disabled"),
            "fieldtype": "Check",
            "width": 80
        }
    ]

def get_data(filters):
    if not filters:
        filters = {}
    
    conditions = get_conditions(filters)
    
    query = """
        SELECT
            i.item_code,
            i.item_name,
            i.item_group,
            COALESCE(SUM(b.actual_qty), 0) as stock_qty,
            COALESCE(SUM(b.stock_value), 0) as stock_value,
            COALESCE(AVG(b.valuation_rate), 0) as valuation_rate,
            COALESCE(i.custom_slow_moving, 0) as slow_moving,
            i.disabled
        FROM `tabItem` i
        LEFT JOIN `tabBin` b ON b.item_code = i.item_code
        WHERE {conditions}
        GROUP BY i.item_code, i.item_name, i.item_group, i.custom_slow_moving, i.disabled
        ORDER BY i.item_code
    """.format(conditions=conditions)
    
    data = frappe.db.sql(query, filters, as_dict=1)
    return data

def get_conditions(filters):
    conditions = []
    conditions.append("i.disabled = 0")
    conditions.append("(COALESCE(b.actual_qty, 0) > 0 OR COALESCE(i.custom_slow_moving, 0) = 1)")
    
    if filters.get("item_code"):
        conditions.append("i.item_code = %(item_code)s")
    
    if filters.get("item_name"):
        conditions.append("i.item_name = %(item_name)s")
    
    if filters.get("item_group"):
        conditions.append("i.item_group = %(item_group)s")
    
    if filters.get("custom_slow_moving"):
        conditions.append("i.custom_slow_moving = %(custom_slow_moving)s")
    
    return " AND ".join(conditions)