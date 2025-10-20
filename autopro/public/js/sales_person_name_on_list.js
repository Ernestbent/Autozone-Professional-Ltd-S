frappe.listview_settings['Sales Order'] = {
    add_fields: ["sales_person", "approved_by", "billed_by"],
    get_indicator: function(doc) {
        if (doc.docstatus === 0) {
            return [__("Draft"), "red", "docstatus,=,0"];
        } else if (doc.docstatus === 1) {
            return [__("Submitted"), "blue", "docstatus,=,1"];
        } else {
            return [__("Cancelled"), "gray", "docstatus,=,2"];
        }
    },
    formatters: {
        sales_person: function(value) {
            return value || "";
        },
        approved_by: function(value) {
            return value || "";
        },
        billed_by: function(value) {
            return value || "";
        }
    }
};