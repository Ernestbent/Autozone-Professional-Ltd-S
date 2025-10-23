# Copyright (c) 2025, Autozone Pro Ltd and contributors
# For license information, please see license.txt

# import frappe


import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    start_date = filters.get("start_date", "2025-10-01")
    end_date = filters.get("end_date", "2025-10-31")

    columns = get_columns()
    data = get_data(start_date, end_date)

    return columns, data


def get_columns():
    return [
        {"label": "Sales Person", "fieldname": "sales_person", "fieldtype": "Link", "options": "Sales Person", "width": 200},
        {"label": "Total Sales Orders", "fieldname": "total_sales_orders", "fieldtype": "Currency", "width": 180},
        {"label": "Net Invoices", "fieldname": "net_invoices", "fieldtype": "Currency", "width": 180},
        {"label": "Total Credit Notes", "fieldname": "total_credit_notes", "fieldtype": "Currency", "width": 180},
        {"label": "Net Sales", "fieldname": "net_sales", "fieldtype": "Currency", "width": 180},
    ]


def get_data(start_date, end_date):
    query = f"""
        SELECT
          sp.name AS sales_person,
          IFNULL(so.total_sales_orders, 0) AS total_sales_orders,
          IFNULL(si.net_amount, 0) AS net_invoices,
          IFNULL(cr.total_credit_notes, 0) AS total_credit_notes,
          (IFNULL(si.net_amount, 0) - IFNULL(cr.total_credit_notes, 0)) AS net_sales
        FROM `tabSales Person` sp
        /* 1) Total Sales Orders for customers linked to sales person */
        LEFT JOIN (
          SELECT
            st.sales_person,
            SUM(so.base_grand_total) AS total_sales_orders
          FROM `tabSales Order` so
          INNER JOIN `tabSales Team` st 
            ON st.parent = so.name 
            AND st.parenttype = 'Sales Order'
          WHERE so.docstatus = 1
            AND so.transaction_date BETWEEN %(start_date)s AND %(end_date)s
          GROUP BY st.sales_person
        ) so ON so.sales_person = sp.name
        /* 2) Net Invoice Amount for customers */
        LEFT JOIN (
          SELECT
            st.sales_person,
            SUM(si.net_total) AS net_amount
          FROM `tabSales Invoice` si
          INNER JOIN `tabSales Team` st 
            ON st.parent = si.name 
            AND st.parenttype = 'Sales Invoice'
          WHERE si.docstatus = 1
            AND IFNULL(si.is_return, 0) = 0
            AND si.posting_date BETWEEN %(start_date)s AND %(end_date)s
          GROUP BY st.sales_person
        ) si ON si.sales_person = sp.name
        /* 3) Total Credit Notes for customers */
        LEFT JOIN (
          SELECT
            st.sales_person,
            SUM(cr.base_grand_total) AS total_credit_notes
          FROM `tabSales Invoice` cr
          INNER JOIN `tabSales Team` st 
            ON st.parent = cr.name 
            AND st.parenttype = 'Sales Invoice'
          WHERE cr.docstatus = 1
            AND IFNULL(cr.is_return, 0) = 1
            AND cr.posting_date BETWEEN %(start_date)s AND %(end_date)s
          GROUP BY st.sales_person
        ) cr ON cr.sales_person = sp.name
        ORDER BY sp.name
    """

    data = frappe.db.sql(query, {"start_date": start_date, "end_date": end_date}, as_dict=True)
    return data
