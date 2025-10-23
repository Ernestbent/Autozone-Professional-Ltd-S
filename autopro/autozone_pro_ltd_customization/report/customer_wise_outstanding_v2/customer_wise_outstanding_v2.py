import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 180},
        {"label": "Voucher Number", "fieldname": "voucher_number", "fieldtype": "Data", "width": 130},
        {"label": "Voucher Date", "fieldname": "voucher_date", "fieldtype": "Date", "width": 100},
        {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 120},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 120},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 120},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "AgeingDays", "fieldname": "ageing_days", "fieldtype": "Int", "width": 100},
        {"label": "Sales Person", "fieldname": "sales_person", "fieldtype": "Data", "width": 150}
    ]


def get_data(filters):
    conditions = ""
    if filters.get("company"):
        conditions += f" AND gl.company = {frappe.db.escape(filters.get('company'))}"
    if filters.get("from_date"):
        conditions += f" AND gl.posting_date >= {frappe.db.escape(filters.get('from_date'))}"
    if filters.get("to_date"):
        conditions += f" AND gl.posting_date <= {frappe.db.escape(filters.get('to_date'))}"

    query = f"""
        SELECT 
            gl.party AS customer_name,
            gl.voucher_no AS voucher_number,
            gl.posting_date AS voucher_date,
            CASE 
                WHEN gl.voucher_type = 'Sales Invoice' AND si.is_return = 1 THEN 'Credit Note'
                ELSE gl.voucher_type
            END AS voucher_type,
            SUM(CASE WHEN acc.account_type = 'Receivable' THEN gl.debit ELSE 0 END) AS debit,
            SUM(CASE WHEN acc.account_type = 'Receivable' THEN gl.credit ELSE 0 END) AS credit,
            SUM(CASE WHEN acc.account_type = 'Receivable' THEN gl.debit - gl.credit ELSE 0 END)
                OVER (PARTITION BY gl.party ORDER BY gl.posting_date, gl.voucher_no) AS balance,
            CASE
                WHEN SUM(CASE WHEN acc.account_type = 'Receivable' THEN gl.debit - gl.credit ELSE 0 END)
                    OVER (PARTITION BY gl.party ORDER BY gl.posting_date, gl.voucher_no) > 0.01 THEN 'Outstanding'
                WHEN SUM(CASE WHEN acc.account_type = 'Receivable' THEN gl.debit - gl.credit ELSE 0 END)
                    OVER (PARTITION BY gl.party ORDER BY gl.posting_date, gl.voucher_no) < -0.01 THEN 'Advance'
                ELSE 'Settled'
            END AS status,
            DATEDIFF(CURDATE(), gl.posting_date) AS ageing_days,
            COALESCE(st.sales_person, 'N/A') AS sales_person
        FROM `tabGL Entry` gl
        LEFT JOIN `tabAccount` acc ON acc.name = gl.account
        LEFT JOIN `tabSales Invoice` si 
            ON si.name = gl.voucher_no AND gl.voucher_type = 'Sales Invoice'
        LEFT JOIN `tabSales Team` st
            ON st.parenttype = 'Customer' AND st.parent = gl.party AND st.idx = 1
        WHERE gl.party_type = 'Customer'
          AND gl.docstatus = 1
          AND IFNULL(gl.is_cancelled, 0) = 0
          {conditions}
        GROUP BY gl.party, gl.voucher_no, gl.posting_date, gl.voucher_type, si.is_return, st.sales_person
        ORDER BY gl.party, gl.posting_date
    """

    return frappe.db.sql(query, as_dict=True)
