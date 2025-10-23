import frappe
from frappe.utils import flt, nowdate

def execute(filters=None):
    if filters is None:
        filters = {}

    data = get_data(filters)
    columns = get_columns()
    return columns, data

def get_columns():
    return [
        {"label": "Sales Order", "fieldname": "sales_order", "fieldtype": "Data", "width": 120},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Data", "width": 200},
        {"label": "Qty Ordered", "fieldname": "qty_ordered", "fieldtype": "Float", "width": 120},
        {"label": "Amount Ordered", "fieldname": "amount_ordered", "fieldtype": "Currency", "width": 120},
        {"label": "Qty Billed", "fieldname": "qty_billed", "fieldtype": "Float", "width": 120},
        {"label": "Amount Billed", "fieldname": "amount_billed", "fieldtype": "Currency", "width": 120},
        {"label": "Qty Diff", "fieldname": "qty_diff", "fieldtype": "Float", "width": 120},
        {"label": "Amount Diff", "fieldname": "amount_diff", "fieldtype": "Currency", "width": 120},
        {"label": "Order Created", "fieldname": "order_created", "fieldtype": "Datetime", "width": 150},
        {"label": "Approval Time", "fieldname": "approval_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Billing Time", "fieldname": "billing_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Turnaround Time", "fieldname": "turnaround_time", "fieldtype": "Data", "width": 150},
        {"label": "Billing Completion %", "fieldname": "billing_completion_percent", "fieldtype": "Float", "width": 120},
        {"label": "Pending Amount", "fieldname": "pending_amount", "fieldtype": "Currency", "width": 120},
    ]

def get_data(filters):
	# Fetch data for the report using SQL
    from_date = filters.get("from_date") or frappe.utils.add_days(nowdate(), -30)
    to_date = filters.get("to_date") or nowdate()

    query = f"""
    WITH billed_per_order AS (
        SELECT
            si_item.sales_order,
            SUM(si_item.qty) AS qty_billed,
            SUM(si_item.base_amount) AS amount_billed,
            MAX(CONCAT(si.posting_date, ' ', si.posting_time)) AS last_billing_datetime
        FROM `tabSales Invoice Item` si_item
        INNER JOIN `tabSales Invoice` si 
            ON si.name = si_item.parent AND si.docstatus = 1
        WHERE si_item.sales_order IS NOT NULL
        GROUP BY si_item.sales_order
    ),
    orders AS (
        SELECT
            so.name AS sales_order,
            so.customer,
            SUM(so_item.qty) AS qty_ordered,
            SUM(so_item.base_amount) AS amount_ordered,
            COALESCE(b.qty_billed, 0) AS qty_billed,
            COALESCE(b.amount_billed, 0) AS amount_billed,
            SUM(so_item.qty) - COALESCE(b.qty_billed, 0) AS qty_diff,
            SUM(so_item.base_amount) - COALESCE(b.amount_billed, 0) AS amount_diff,
            DATE_FORMAT(so.creation, '%Y-%m-%d %H:%i') AS order_created,
            DATE_FORMAT(so.modified, '%Y-%m-%d %H:%i') AS approval_time,
            DATE_FORMAT(b.last_billing_datetime, '%Y-%m-%d %H:%i') AS billing_time,
            CONCAT(
                FLOOR(TIMESTAMPDIFF(SECOND, so.creation, b.last_billing_datetime)/3600), ' hrs ',
                FLOOR((TIMESTAMPDIFF(SECOND, so.creation, b.last_billing_datetime) % 3600)/60), ' mins'
            ) AS turnaround_time,
            ROUND((COALESCE(b.qty_billed,0)/SUM(so_item.qty))*100,2) AS billing_completion_percent,
            SUM(so_item.base_amount) - COALESCE(b.amount_billed,0) AS pending_amount
        FROM `tabSales Order` so
        INNER JOIN `tabSales Order Item` so_item 
            ON so_item.parent = so.name
        LEFT JOIN billed_per_order b 
            ON b.sales_order = so.name
        WHERE so.transaction_date BETWEEN '{from_date}' AND '{to_date}'
          AND so.docstatus = 1
        GROUP BY so.name, so.customer
    )
    SELECT *
    FROM (
        SELECT *
        FROM orders

        UNION ALL

        SELECT
            'TOTAL' AS sales_order,
            '-' AS customer,
            SUM(orders.qty_ordered),
            SUM(orders.amount_ordered),
            SUM(orders.qty_billed),
            SUM(orders.amount_billed),
            SUM(orders.qty_diff),
            SUM(orders.amount_diff),
            NULL, NULL, NULL,
            CONCAT(
                FLOOR(SUM(TIMESTAMPDIFF(SECOND, STR_TO_DATE(orders.order_created, '%Y-%m-%d %H:%i'),
                STR_TO_DATE(orders.billing_time, '%Y-%m-%d %H:%i')))/3600), ' hrs ',
                FLOOR((SUM(TIMESTAMPDIFF(SECOND, STR_TO_DATE(orders.order_created, '%Y-%m-%d %H:%i'),
                STR_TO_DATE(orders.billing_time, '%Y-%m-%d %H:%i'))) % 3600)/60), ' mins'
            ) AS turnaround_time,
            ROUND(SUM(orders.qty_billed)/SUM(orders.qty_ordered)*100,2) AS billing_completion_percent,
            SUM(orders.pending_amount)
        FROM orders
    ) AS final
    ORDER BY
        CASE WHEN sales_order = 'TOTAL' THEN 1 ELSE 0 END,
        order_created ASC
    """

    return frappe.db.sql(query, as_dict=True)
