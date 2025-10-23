# Copyright (c) 2025, Autozone Pro Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType, functions as fn

def execute(filters=None):
    filters = filters or {}

    # Define DocTypes
    so = DocType("Sales Order")
    c = DocType("Comment")

    # Main query using Pypika
    query = (
        frappe.qb.from_(so)
        .left_join(c).on(
            (c.reference_doctype == "Sales Order")
            & (c.reference_name == so.name)
            & (c.comment_type == "Workflow")
            & (c.content == "Dispatched")
        )
        .select(
            so.transaction_date.as_("Sales Order Date"),
            so.name.as_("Sales Order No"),
            so.workflow_state.as_("Status"),
            so.customer_name.as_("Customer Name"),
            c.creation.as_("Dispatched Date"),
            c.owner.as_("Dispatched By"),
        )
        .where((so.docstatus == 1) & (so.workflow_state == "Dispatched"))
    )

    # Apply filters to main query
    if filters.get("from_date") and filters.get("to_date"):
        query = query.where(so.transaction_date.between(filters.get("from_date"), filters.get("to_date")))
    if filters.get("customer"):
        query = query.where(so.customer == filters.get("customer"))
    if filters.get("sales_order"):
        query = query.where(so.name == filters.get("sales_order"))
    if filters.get("dispatched_by"):
        query = query.where(c.owner == filters.get("dispatched_by"))

    # Apply pagination
    limit_page_length = filters.get("limit_page_length", 100)
    limit_start = filters.get("start", 0)
    query = query.limit(limit_page_length).offset(limit_start).orderby(so.transaction_date, order=frappe.qb.desc)

    # Execute main query
    base_data = query.run(as_dict=True)

    # Get Delivery Notes using raw SQL
    dn_query = """
        SELECT 
            soi.parent AS sales_order,
            GROUP_CONCAT(DISTINCT dn.name) AS delivery_notes,
            SUM(DISTINCT dni.qty) AS total_billed_qty
        FROM `tabSales Order Item` soi
        INNER JOIN `tabDelivery Note Item` dni ON dni.so_detail = soi.name
        INNER JOIN `tabDelivery Note` dn ON dn.name = dni.parent AND dn.docstatus = 1
        {dn_filter}
        GROUP BY soi.parent
    """
    dn_filter = ""
    if filters.get("delivery_note"):
        dn_filter = f"AND dn.name = '{frappe.db.escape(filters.get('delivery_note'))}'"
    dn_query = dn_query.format(dn_filter=dn_filter)
    delivery_map = {row['sales_order']: row for row in frappe.db.sql(dn_query, as_dict=True)}

    # Get Sales Invoices using raw SQL
    si_query = """
        SELECT 
            soi.parent AS sales_order,
            GROUP_CONCAT(DISTINCT si.name) AS sales_invoices,
            SUM(DISTINCT si.grand_total) AS invoice_amount
        FROM `tabSales Order Item` soi
        INNER JOIN `tabSales Invoice Item` sii ON sii.so_detail = soi.name
        INNER JOIN `tabSales Invoice` si ON si.name = sii.parent AND si.docstatus = 1
        {si_filter}
        GROUP BY soi.parent
    """
    si_filter = ""
    if filters.get("sales_invoice"):
        si_filter = f"AND si.name = '{frappe.db.escape(filters.get('sales_invoice'))}'"
    si_query = si_query.format(si_filter=si_filter)
    invoice_map = {row['sales_order']: row for row in frappe.db.sql(si_query, as_dict=True)}

    # Merge results
    results = []
    for row in base_data:
        sales_order = row["Sales Order No"]
        
        # Add Delivery Notes
        dn_row = delivery_map.get(sales_order, {})
        row["Delivery Note No"] = dn_row.get("delivery_notes", "")
        row["Total Billed Qty"] = dn_row.get("total_billed_qty", 0)
        
        # Add Sales Invoices
        si_row = invoice_map.get(sales_order, {})
        row["Sales Invoice No"] = si_row.get("sales_invoices", "")
        row["Invoice Amount"] = si_row.get("invoice_amount", 0)
        
        results.append(row)

    # Define columns to be shown
    columns = [
        {"label": "Sales Order Date", "fieldname": "Sales Order Date", "fieldtype": "Date", "width": 100},
        {"label": "Sales Order No", "fieldname": "Sales Order No", "fieldtype": "Link", "options": "Sales Order", "width": 150},
        {"label": "Delivery Note No", "fieldname": "Delivery Note No", "fieldtype": "Data", "width": 150},
        {"label": "Sales Invoice No", "fieldname": "Sales Invoice No", "fieldtype": "Data", "width": 150},
        {"label": "Dispatched Date", "fieldname": "Dispatched Date", "fieldtype": "Datetime", "width": 150},
        {"label": "Dispatched By", "fieldname": "Dispatched By", "fieldtype": "Link", "options": "User", "width": 120},
        {"label": "Total Billed Qty", "fieldname": "Total Billed Qty", "fieldtype": "Float", "width": 120},
        {"label": "Invoice Amount", "fieldname": "Invoice Amount", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "Status", "fieldtype": "Data", "width": 120},
        {"label": "Customer Name", "fieldname": "Customer Name", "fieldtype": "Data", "width": 200},
    ]

    return columns, results