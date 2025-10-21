# Copyright (c) 2025, Autozone Pro Ltd and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe.query_builder import DocType, functions as fn

def execute(filters=None):
    filters = filters or {}

    # Define the doctypes to be used in the query
    SI = DocType("Sales Invoice")
    SII = DocType("Sales Invoice Item")
    SO = DocType("Sales Order")
    DN = DocType("Delivery Note")
    I = DocType("Item")
    ST = DocType("Sales Team")
    C = DocType("Customer")

    # Subquery to calculate grand total before discount
    sii_inner = DocType("Sales Invoice Item")
    subquery_total_before_discount = (
        frappe.qb.from_(sii_inner)
        .select(
            (fn.Sum(
                sii_inner.qty * sii_inner.rate / 
                (1 - fn.IfNull(sii_inner.discount_percentage, 0) / 100)
            ) + fn.IfNull(SI.discount_amount, 0)).as_("grand_total_before_discount")
        )
        .where(sii_inner.parent == SI.name)
    )

    # Main query
    query = (
        frappe.qb.from_(SI)
        .join(SII).on(SII.parent == SI.name)
        .left_join(SO).on(SII.sales_order == SO.name)
        .left_join(DN).on(SII.delivery_note == DN.name)
        .left_join(I).on(SII.item_code == I.name)
        .left_join(ST).on(SI.name == ST.parent)
        .left_join(C).on(SI.customer == C.name)
        .select(
            SII.item_code.as_("item_code"),
            SII.item_name.as_("item_description"),
            SO.transaction_date.as_("sales_order_date"),
            SI.posting_date.as_("invoice_date"),
            DN.posting_date.as_("delivery_date"),
            SI.name.as_("invoice_number"),
            SI.customer.as_("customer_id"),
            SO.name.as_("sales_order_number"),
            DN.name.as_("delivery_note_number"),
            SII.qty.as_("billed_quantity"),
            I.standard_rate.as_("standard_selling_price"),
            SII.rate.as_("rate_amount"),
            SII.amount.as_("total_amount_with_discount"),
            (SII.qty * SII.rate / (1 - fn.IfNull(SII.discount_percentage, 0) / 100)).as_("total_amount_without_discount"),
            SII.discount_percentage.as_("discount_percentage"),
            fn.GroupConcat(ST.sales_person).as_("sales_person"),
            fn.Lower(fn.Coalesce(C.district, "")).as_("district"),
            fn.Lower(fn.Coalesce(C.region, "")).as_("region"),
            fn.Lower(fn.Coalesce(C.route, "")).as_("route"),
            SI.grand_total.as_("grand_total_after_discount"),
            subquery_total_before_discount.as_("grand_total_before_discount"),
        )
        .where(SI.docstatus == 1)
        .groupby(SII.name, SI.name, SO.name, DN.name, C.name)
        .orderby(SI.posting_date, order=frappe.qb.desc)
    )

    data = query.run(as_dict=True)

    # Define columns
    columns = [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Data", "width": 120},
        {"label": "Item Description", "fieldname": "item_description", "fieldtype": "Data", "width": 200},
        {"label": "Sales Order Date", "fieldname": "sales_order_date", "fieldtype": "Date", "width": 120},
        {"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 120},
        {"label": "Delivery Date", "fieldname": "delivery_date", "fieldtype": "Date", "width": 120},
        {"label": "Invoice Number", "fieldname": "invoice_number", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
        {"label": "Customer ID", "fieldname": "customer_id", "fieldtype": "Link", "options": "Customer", "width": 140},
        {"label": "Sales Order Number", "fieldname": "sales_order_number", "fieldtype": "Link", "options": "Sales Order", "width": 150},
        {"label": "Delivery Note Number", "fieldname": "delivery_note_number", "fieldtype": "Link", "options": "Delivery Note", "width": 150},
        {"label": "Billed Quantity", "fieldname": "billed_quantity", "fieldtype": "Float", "width": 110},
        {"label": "Standard Selling Price", "fieldname": "standard_selling_price", "fieldtype": "Currency", "width": 140},
        {"label": "Rate Amount", "fieldname": "rate_amount", "fieldtype": "Currency", "width": 140},
        {"label": "Total Amount With Discount", "fieldname": "total_amount_with_discount", "fieldtype": "Currency", "width": 160},
        {"label": "Total Amount Without Discount", "fieldname": "total_amount_without_discount", "fieldtype": "Currency", "width": 180},
        {"label": "Discount %", "fieldname": "discount_percentage", "fieldtype": "Float", "width": 100},
        {"label": "Sales Person", "fieldname": "sales_person", "fieldtype": "Data", "width": 140},
        {"label": "District", "fieldname": "district", "fieldtype": "Data", "width": 120},
        {"label": "Region", "fieldname": "region", "fieldtype": "Data", "width": 120},
        {"label": "Route", "fieldname": "route", "fieldtype": "Data", "width": 120},
        {"label": "Grand Total After Discount", "fieldname": "grand_total_after_discount", "fieldtype": "Currency", "width": 180},
        {"label": "Grand Total Before Discount", "fieldname": "grand_total_before_discount", "fieldtype": "Currency", "width": 180},
    ]

    return columns, data

