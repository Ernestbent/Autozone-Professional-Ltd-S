frappe.query_reports["Unlinked Payment Report v2"] = {
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
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": "150"
        },
        {
            "fieldname": "amount_status",
            "label": __("Amount Status"),
            "fieldtype": "Select",
            "options": ["All", "Unallocated", "Excess Money"],
            "default": "All"
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
            "fieldname": "row_limit",
            "label": __("Rows"),
            "fieldtype": "Select",
            "options": ["20", "100", "500", "All"],
            "default": "100"
        }
    ],
    "columns": [
        {"fieldname": "document_type", "label": __("Document Type"), "fieldtype": "Data", "width": 140},
        {"fieldname": "document_name", "label": __("Document Name"), "fieldtype": "HTML", "width": 180},
        {"fieldname": "customer", "label": __("Customer"), "fieldtype": "HTML", "width": 220},
        {"fieldname": "posting_date", "label": __("Posting Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "amount", "label": __("Amount"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "amount_status", "label": __("Amount Status"), "fieldtype": "Data", "width": 140},
        {"fieldname": "unallocated_amount", "label": __("Unallocated Amount"), "fieldtype": "Currency", "width": 160},
        {"fieldname": "to_account", "label": __("To Account"), "fieldtype": "Data", "width": 200}
    ]
};