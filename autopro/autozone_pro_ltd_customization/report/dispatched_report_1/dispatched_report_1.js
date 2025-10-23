frappe.query_reports["Dispatched Report 1"] = {
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
            "reqd": 0
        },
        {
            "fieldname": "sales_order",
            "label": __("Sales Order"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "reqd": 0
        },
        {
            "fieldname": "delivery_note",
            "label": __("Delivery Note"),
            "fieldtype": "Link",
            "options": "Delivery Note",
            "reqd": 0
        },
        {
            "fieldname": "sales_invoice",
            "label": __("Sales Invoice"),
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "reqd": 0
        },
        {
            "fieldname": "dispatched_by",
            "label": __("Dispatched By"),
            "fieldtype": "Link",
            "options": "User",
            "reqd": 0
        }
    ]
}