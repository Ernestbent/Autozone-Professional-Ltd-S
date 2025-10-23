frappe.query_reports["Billed Report v2"] = {
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
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "default": "Main Loc - APL"
        },
        {
            "fieldname": "item_code",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item"
        },
        {
            "fieldname": "brand",
            "label": __("Brand"),
            "fieldtype": "Link",
            "options": "Brand"
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "sales_person",
            "label": __("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person"
        },
        {
            "fieldname": "row_limit",
            "label": __("Rows"),
            "fieldtype": "Select",
            "options": "\n20\n100\n500\nAll",
            "default": "100"
        }
    ],
    "columns": [
        {"fieldname": "invoice_date", "label": __("Invoice Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "invoice_number", "label": __("Invoice Number"), "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"fieldname": "customer_id", "label": __("Customer"), "fieldtype": "Link", "options": "Customer", "width": 120},
        {"fieldname": "item_code", "label": __("Item Code"), "fieldtype": "Link", "options": "Item", "width": 120},
        {"fieldname": "description", "label": __("Description"), "fieldtype": "Data", "width": 200},
        {"fieldname": "brand", "label": __("Brand"), "fieldtype": "Data", "width": 120},
        {"fieldname": "model", "label": __("Model"), "fieldtype": "Data", "width": 120},
        {"fieldname": "quantity_billed", "label": __("Quantity Billed"), "fieldtype": "Float", "width": 120},
        {"fieldname": "rate_amount", "label": __("Rate Amount"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "total_amount", "label": __("Total Amount"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "warehouse", "label": __("Warehouse"), "fieldtype": "Link", "options": "Warehouse", "width": 120},
        {"fieldname": "invoice_total", "label": __("Invoice Total"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "sales_person", "label": __("Sales Person"), "fieldtype": "Data", "width": 150}
    ]
};