frappe.query_reports["GL Entry Summary"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        },
        {
            "fieldname": "account",
            "label": __("Account"),
            "fieldtype": "Link",
            "options": "Account",
            "width": "150"
        },
        {
            "fieldname": "finance_book",
            "label": __("Finance Book"),
            "fieldtype": "Link",
            "options": "Finance Book",
            "width": "150"
        },
        {
            "fieldname": "row_limit",
            "label": __("Rows"),
            "fieldtype": "Select",
            "options": ["20", "100", "500", "All"],
            "default": "100"
        }
    ],
    "columns": [
        {"fieldname": "fiscal_year", "label": __("Fiscal Year"), "fieldtype": "Data", "width": 80},
        {"fieldname": "company", "label": __("Company"), "fieldtype": "Data", "width": 220},
        {"fieldname": "posting_date", "label": __("Posting Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "account", "label": __("Account"), "fieldtype": "Link", "options": "Account", "width": 380},
        {"fieldname": "debit", "label": __("Debit"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "credit", "label": __("Credit"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "finance_book", "label": __("Finance Book"), "fieldtype": "Link", "options": "Finance Book", "width": 140}
    ]
};