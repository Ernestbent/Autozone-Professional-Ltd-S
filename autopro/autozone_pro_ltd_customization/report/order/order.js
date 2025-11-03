frappe.query_reports["Sales Invoice Detail Report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            fieldname: "customer",
            label: __("Customer"),
            fieldtype: "Link",
            options: "Customer"
        },
        {
            fieldname: "item_code",
            label: __("Item Code"),
            fieldtype: "Link",
            options: "Item"
        },
        {
            fieldname: "sales_person",
            label: __("Sales Person"),
            fieldtype: "Link",
            options: "Sales Person"
        }
    ],

    formatter: function (row, cell, value, columnDef, data, default_formatter) {
        value = default_formatter(row, cell, value, columnDef, data);

        // Highlight high discount
        if (columnDef.fieldname === "discount_percentage" && value > 10) {
            value = `<span style="color: red; font-weight: bold;">${value}</span>`;
        }

        // Highlight missing delivery
        if (columnDef.fieldname === "delivery_note_number" && !value) {
            value = `<span style="color: orange;">—</span>`;
        }

        return value;
    }
};