import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
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


def get_data(filters):
    return frappe.db.sql(
        """
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

        ORDER BY posting_date DESC
        """,
        filters,
        as_dict=True,
    )
