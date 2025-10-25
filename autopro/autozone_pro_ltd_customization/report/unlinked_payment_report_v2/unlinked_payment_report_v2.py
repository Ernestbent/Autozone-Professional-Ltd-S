# Copyright (c) 2025, Autozone Pro Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, add_months

def execute(filters=None):
    if not filters:
        filters = {}

    # Default values for filters
    from_date = filters.get("from_date", add_months(today(), -1))
    to_date = filters.get("to_date", today())
    customer = filters.get("customer")
    amount_status = filters.get("amount_status")
    company = filters.get("company")
    row_limit = filters.get("row_limit", "100")

    columns = get_columns()
    data = get_data(from_date, to_date, customer, amount_status, company, row_limit)

    return columns, data


def get_columns():
    return [
        {"label": "Document Type", "fieldname": "document_type", "fieldtype": "Data", "width": 140},
        {"label": "Document Name", "fieldname": "document_name", "fieldtype": "HTML", "width": 180},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "HTML", "width": 220},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 140},
        {"label": "Amount Status", "fieldname": "amount_status", "fieldtype": "Data", "width": 140},
        {"label": "Unallocated Amount", "fieldname": "unallocated_amount", "fieldtype": "Currency", "width": 160},
        {"label": "To Account", "fieldname": "to_account", "fieldtype": "Data", "width": 200},
    ]


def get_data(from_date, to_date, customer=None, amount_status=None, company=None, row_limit="100"):
    conditions = []
    params = {"from_date": from_date, "to_date": to_date}

    # Apply customer filter to each section individually
    pe_customer_condition = "pe.party = %(customer)s" if customer else "1=1"
    jea_customer_condition = "jea.party = %(customer)s" if customer else "1=1"
    gl_customer_condition = "gl.party = %(customer)s" if customer else "1=1"
    si_customer_condition = "si.customer = %(customer)s" if customer else "1=1"

    # Company filter
    if company:
        conditions.append("pe.company = %(company)s")
        conditions.append("je.company = %(company)s")
        conditions.append("gl.company = %(company)s")
        conditions.append("si.company = %(company)s")
        params["company"] = company

    query = f"""
        SELECT 
            'Payment Entry' as document_type,
            CONCAT('<a href="/app/payment-entry/', pe.name, '" target="_blank">', pe.name, '</a>') as document_name,
            CONCAT('<a href="/app/customer/', pe.party, '" target="_blank">', pe.party, '</a>') as customer,
            pe.posting_date,
            pe.paid_amount as amount,
            CASE 
                WHEN EXISTS (
                    SELECT 1 FROM `tabSales Invoice` si 
                    WHERE si.customer = pe.party 
                    AND si.docstatus = 1 
                    AND si.is_return = 0 
                    AND si.outstanding_amount > 0
                ) OR EXISTS (
                    SELECT 1 FROM `tabJournal Entry` je
                    INNER JOIN `tabJournal Entry Account` jea ON jea.parent = je.name
                    WHERE jea.party = pe.party
                    AND je.docstatus = 1
                    AND je.is_opening = 'Yes'
                    AND jea.debit > 0
                    AND (jea.debit - COALESCE((
                        SELECT SUM(per.allocated_amount)
                        FROM `tabPayment Entry Reference` per
                        WHERE per.reference_doctype = 'Journal Entry' 
                        AND per.reference_name = je.name
                        AND per.docstatus = 1
                    ), 0)) > 0
                ) THEN 'Unallocated'
                ELSE 'Excess Money'
            END as amount_status,
            pe.unallocated_amount,
            pt.account_name as to_account
        FROM `tabPayment Entry` pe
        LEFT JOIN `tabAccount` pt ON pe.paid_to = pt.name
        WHERE pe.docstatus = 1 
            AND pe.unallocated_amount > 0
            AND pe.party_type = 'Customer'
            AND pe.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND {pe_customer_condition}
    """

    # Add company condition to Payment Entry
    if company:
        query += " AND pe.company = %(company)s"

    query += f"""
        UNION ALL

        SELECT
            'Opening Balance' as document_type,
            CONCAT('<a href="/app/journal-entry/', je.name, '" target="_blank">', je.name, '</a>') as document_name,
            CONCAT('<a href="/app/customer/', jea.party, '" target="_blank">', jea.party, '</a>') as customer,
            je.posting_date,
            jea.credit as amount,
            CASE 
                WHEN EXISTS (
                    SELECT 1 FROM `tabSales Invoice` si 
                    WHERE si.customer = jea.party 
                    AND si.docstatus = 1 
                    AND si.is_return = 0 
                    AND si.outstanding_amount > 0
                ) OR EXISTS (
                    SELECT 1 FROM `tabJournal Entry` je2
                    INNER JOIN `tabJournal Entry Account` jea2 ON jea2.parent = je2.name
                    WHERE jea2.party = jea.party
                    AND je2.docstatus = 1
                    AND je2.is_opening = 'Yes'
                    AND jea2.debit > 0
                    AND (jea2.debit - COALESCE((
                        SELECT SUM(per.allocated_amount)
                        FROM `tabPayment Entry Reference` per
                        WHERE per.reference_doctype = 'Journal Entry' 
                        AND per.reference_name = je2.name
                        AND per.docstatus = 1
                    ), 0)) > 0
                ) THEN 'Unallocated'
                ELSE 'Excess Money'
            END as amount_status,
            jea.credit as unallocated_amount,
            acc.account_name as to_account
        FROM `tabJournal Entry` je
        INNER JOIN `tabJournal Entry Account` jea ON jea.parent = je.name
        LEFT JOIN `tabAccount` acc ON jea.account = acc.name
        WHERE je.docstatus = 1
            AND je.is_opening = 'Yes'
            AND jea.party_type = 'Customer'
            AND jea.party IS NOT NULL
            AND jea.credit > 0
            AND je.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND {jea_customer_condition}
    """

    # Add company condition to Journal Entry
    if company:
        query += " AND je.company = %(company)s"

    query += f"""
        UNION ALL

        SELECT
            'Opening Balance (GL)' as document_type,
            CONCAT('<a href="/app/gl-entry/', gl.name, '" target="_blank">', gl.name, '</a>') as document_name,
            CONCAT('<a href="/app/customer/', gl.party, '" target="_blank">', gl.party, '</a>') as customer,
            gl.posting_date,
            gl.credit as amount,
            CASE 
                WHEN EXISTS (
                    SELECT 1 FROM `tabSales Invoice` si 
                    WHERE si.customer = gl.party 
                    AND si.docstatus = 1 
                    AND si.is_return = 0 
                    AND si.outstanding_amount > 0
                ) OR EXISTS (
                    SELECT 1 FROM `tabJournal Entry` je
                    INNER JOIN `tabJournal Entry Account` jea ON jea.parent = je.name
                    WHERE jea.party = gl.party
                    AND je.docstatus = 1
                    AND je.is_opening = 'Yes'
                    AND jea.debit > 0
                    AND (jea.debit - COALESCE((
                        SELECT SUM(per.allocated_amount)
                        FROM `tabPayment Entry Reference` per
                        WHERE per.reference_doctype = 'Journal Entry' 
                        AND per.reference_name = je.name
                        AND per.docstatus = 1
                    ), 0)) > 0
                ) THEN 'Unallocated'
                ELSE 'Excess Money'
            END as amount_status,
            gl.credit as unallocated_amount,
            acc.account_name as to_account
        FROM `tabGL Entry` gl
        LEFT JOIN `tabAccount` acc ON gl.account = acc.name
        WHERE gl.docstatus = 1
            AND gl.party_type = 'Customer'
            AND gl.party IS NOT NULL
            AND gl.credit > 0
            AND gl.is_opening = 'Yes'
            AND NOT EXISTS (
                SELECT 1 FROM `tabJournal Entry Account` jea 
                WHERE jea.name = gl.voucher_detail_no
                AND jea.parent = gl.voucher_no
            )
            AND gl.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND {gl_customer_condition}
    """

    # Add company condition to GL Entry
    if company:
        query += " AND gl.company = %(company)s"

    query += f"""
        UNION ALL

        SELECT
            'Credit Note' as document_type,
            CONCAT('<a href="/app/sales-invoice/', si.name, '" target="_blank">', si.name, '</a>') as document_name,
            CONCAT('<a href="/app/customer/', si.customer, '" target="_blank">', si.customer, '</a>') as customer,
            si.posting_date,
            si.grand_total as amount,
            CASE 
                WHEN EXISTS (
                    SELECT 1 FROM `tabSales Invoice` si2 
                    WHERE si2.customer = si.customer 
                    AND si2.docstatus = 1 
                    AND si2.is_return = 0 
                    AND si2.outstanding_amount > 0
                ) OR EXISTS (
                    SELECT 1 FROM `tabJournal Entry` je
                    INNER JOIN `tabJournal Entry Account` jea ON jea.parent = je.name
                    WHERE jea.party = si.customer
                    AND je.docstatus = 1
                    AND je.is_opening = 'Yes'
                    AND jea.debit > 0
                    AND (jea.debit - COALESCE((
                        SELECT SUM(per.allocated_amount)
                        FROM `tabPayment Entry Reference` per
                        WHERE per.reference_doctype = 'Journal Entry' 
                        AND per.reference_name = je.name
                        AND per.docstatus = 1
                    ), 0)) > 0
                ) THEN 'Unallocated'
                ELSE 'Excess Money'
            END as amount_status,
            si.outstanding_amount as unallocated_amount,
            '' as to_account
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1 
            AND si.is_return = 1
            AND si.outstanding_amount < 0
            AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND {si_customer_condition}
    """

    # Add company condition to Sales Invoice
    if company:
        query += " AND si.company = %(company)s"

    # Order by and limit
    query += """
        ORDER BY posting_date DESC
    """

    # Apply row limit
    if row_limit != "All":
        query += " LIMIT %(row_limit)s"
        params["row_limit"] = int(row_limit)
    else:
        query += " LIMIT 10000"  # Safety limit to prevent performance issues

    if customer:
        params["customer"] = customer

    data = frappe.db.sql(query, params, as_dict=True)

    # Apply amount_status filter post-query if specified
    if amount_status and amount_status != "All":
        data = [row for row in data if row["amount_status"] == amount_status]

    return data