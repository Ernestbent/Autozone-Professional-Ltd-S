frappe.query_reports["Sales Invoice Detailed Report v2"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -30),
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 0
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "reqd": 0
        },
        {
            "fieldname": "item_code",
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
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
            "fieldname": "district",
            "label": __("District"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "region",
            "label": __("Region"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "route",
            "label": __("Route"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "sales_person",
            "label": __("Sales Person"),
            "fieldtype": "Data",
            "reqd": 0
        }
    ]
}