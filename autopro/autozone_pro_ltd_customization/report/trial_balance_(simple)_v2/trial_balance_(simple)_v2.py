import frappe
from frappe.query_builder import DocType, functions as fn

def execute(filters=None):
    filters = filters or {}

    company = filters.get("company")

    # Define Doctype
    GL = DocType("GL Entry")

    # Build query
    query = (
        frappe.qb.from_(GL)
        .select(
            GL.fiscal_year.as_("fiscal_year"),
            GL.company.as_("company"),
            GL.posting_date.as_("posting_date"),
            GL.account.as_("account"),
            fn.Sum(GL.debit).as_("debit"),
            fn.Sum(GL.credit).as_("credit"),
            GL.finance_book.as_("finance_book")
        )
        .where(GL.is_cancelled == 0)
        .groupby(
            GL.fiscal_year,
            GL.company,
            GL.posting_date,
            GL.account,
        )
        .orderby(
            GL.fiscal_year,
            GL.company,
            GL.posting_date,
            GL.account
        )
    )

    # Apply company filter if provided
    if company:
        query = query.where(GL.company == company)

    # Execute the query
    data = query.run(as_dict=True)

    # Define columns for ERPNext report
    columns = [
        {"label": "Fiscal Year", "fieldname": "fiscal_year", "fieldtype": "Data", "width": 80},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 220},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 380},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 140},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 140},
        {"label": "Finance Book", "fieldname": "finance_book", "fieldtype": "Link", "options": "Finance Book", "width": 140},
    ]

    return columns, data
