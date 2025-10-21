import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Total Billed", "fieldname": "total_billed", "fieldtype": "Currency", "width": 150},
        {"label": "Total Paid", "fieldname": "total_paid", "fieldtype": "Currency", "width": 150},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 150},
        {"label": "Status", "fieldname": "advance_or_outstanding", "fieldtype": "Data", "width": 150},
        {"label": "Latest Invoices", "fieldname": "latest_invoices", "fieldtype": "Data", "width": 300},
    ]


def get_data():
    # Main SQL Query
    query = """
        SELECT
            gl.party AS customer,
            SUM(gl.debit) AS total_billed,
            SUM(gl.credit) AS total_paid,
            SUM(gl.debit - gl.credit) AS balance,
            CASE
                WHEN SUM(gl.debit - gl.credit) < 0 THEN 'Advance'
                WHEN SUM(gl.debit - gl.credit) > 0 THEN 'Outstanding'
                ELSE 'Settled'
            END AS advance_or_outstanding,
            COALESCE(inv.latest_invoices, 'No Invoice') AS latest_invoices
        FROM `tabGL Entry` gl
        LEFT JOIN (
            SELECT
                si.customer,
                GROUP_CONCAT(si.name ORDER BY si.posting_date DESC SEPARATOR ', ') AS latest_invoices
            FROM `tabSales Invoice` si
            WHERE si.docstatus = 1
            GROUP BY si.customer
        ) AS inv ON inv.customer = gl.party
        WHERE
            gl.party_type = 'Customer'
            AND gl.docstatus = 1
        GROUP BY gl.party, inv.latest_invoices
        ORDER BY gl.party
    """

    return frappe.db.sql(query, as_dict=True)
