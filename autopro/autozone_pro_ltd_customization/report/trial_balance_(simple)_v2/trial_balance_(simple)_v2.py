# Copyright (c) 2025, Autozone Pro Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType, functions as fn
from frappe.utils import today, add_months

def execute(filters=None):
    filters = filters or {}

    # Default values for filters
    from_date = filters.get("from_date", add_months(today(), -1))
    to_date = filters.get("to_date", today())
    company = filters.get("company")
    account = filters.get("account")
    finance_book = filters.get("finance_book")
    row_limit = filters.get("row_limit", "100")

    columns = get_columns()
    data = get_data(from_date, to_date, company, account, finance_book, row_limit)

    return columns, data


def get_columns():
    return [
        {"label": "Fiscal Year", "fieldname": "fiscal_year", "fieldtype": "Data", "width": 80},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 220},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 380},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 140},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 140},
        {"label": "Finance Book", "fieldname": "finance_book", "fieldtype": "Link", "options": "Finance Book", "width": 140},
    ]


def get_data(from_date, to_date, company=None, account=None, finance_book=None, row_limit="100"):
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
        .where(GL.posting_date.between(from_date, to_date))
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

    # Apply filters
    if company:
        query = query.where(GL.company == company)
    if account:
        query = query.where(GL.account == account)
    if finance_book:
        query = query.where(GL.finance_book == finance_book)
    if row_limit != "All":
        query = query.limit(int(row_limit))
    else:
        query = query.limit(10000)  # Safety limit to prevent performance issues

    # Execute the query
    data = query.run(as_dict=True)

    return data