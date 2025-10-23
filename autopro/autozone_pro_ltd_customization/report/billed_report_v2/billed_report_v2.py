# -*- coding: utf-8 -*-
# Copyright (c) 2025, Autozone Pro Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType, functions as fn
from frappe.utils import today, add_months

def execute(filters=None):
    if filters is None:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "invoice_date", "label": "Invoice Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "invoice_number", "label": "Invoice Number", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"fieldname": "customer_id", "label": "Customer", "fieldtype": "Link", "options": "Customer", "width": 120},
        {"fieldname": "item_code", "label": "Item Code", "fieldtype": "Link", "options": "Item", "width": 120},
        {"fieldname": "description", "label": "Description", "fieldtype": "Data", "width": 200},
        {"fieldname": "brand", "label": "Brand", "fieldtype": "Data", "width": 120},
        {"fieldname": "model", "label": "Model", "fieldtype": "Data", "width": 120},
        {"fieldname": "quantity_billed", "label": "Quantity Billed", "fieldtype": "Float", "width": 120},
        {"fieldname": "rate_amount", "label": "Rate Amount", "fieldtype": "Currency", "width": 120},
        {"fieldname": "total_amount", "label": "Total Amount", "fieldtype": "Currency", "width": 140},
        {"fieldname": "warehouse", "label": "Warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 120},
        {"fieldname": "invoice_total", "label": "Invoice Total", "fieldtype": "Currency", "width": 140},
        {"fieldname": "sales_person", "label": "Sales Person", "fieldtype": "Data", "width": 150}
    ]

def get_data(filters):
    # Define DocTypes
    SI = DocType("Sales Invoice")
    SII = DocType("Sales Invoice Item")
    I = DocType("Item")
    ST = DocType("Sales Team")

    # Build query
    query = (
        frappe.qb.from_(SI)
        .join(SII).on(SII.parent == SI.name)
        .left_join(I).on(SII.item_code == I.name)
        .left_join(ST).on(SI.name == ST.parent)
        .select(
            SI.posting_date.as_("invoice_date"),
            SI.name.as_("invoice_number"),
            SI.customer.as_("customer_id"),
            SII.item_code.as_("item_code"),
            SII.description.as_("description"),
            I.brand.as_("brand"),
            fn.Coalesce(I.custom_model, "").as_("model"),
            SII.qty.as_("quantity_billed"),
            SII.rate.as_("rate_amount"),
            (SII.qty * SII.rate).as_("total_amount"),
            SII.warehouse.as_("warehouse"),
            SI.grand_total.as_("invoice_total"),
            fn.GroupConcat(ST.sales_person).as_("sales_person")
        )
        .where(SI.docstatus == 1)
    )

    # Apply filters
    from_date = filters.get("from_date") or add_months(today(), -1)
    to_date = filters.get("to_date") or today()
    query = query.where(SI.posting_date.between(from_date, to_date))

    if filters.get("item_code"):
        query = query.where(SII.item_code == filters.get("item_code"))

    if filters.get("brand"):
        query = query.where(I.brand == filters.get("brand"))

    if filters.get("warehouse"):
        query = query.where(SII.warehouse == filters.get("warehouse"))

    if filters.get("customer"):
        query = query.where(SI.customer == filters.get("customer"))

    if filters.get("sales_person"):
        query = query.where(ST.sales_person == filters.get("sales_person"))

    # Apply row limit
    row_limit = filters.get("row_limit", "100")
    if row_limit != "All":
        query = query.limit(int(row_limit))
    else:
        query = query.limit(10000)  # Safety limit to prevent performance issues

    # Group and order
    query = query.groupby(SI.name, SII.name)
    query = query.orderby(SI.posting_date, order=frappe.qb.desc)
    query = query.orderby(SI.name)

    # Execute query
    data = query.run(as_dict=True)

    return data