frappe.listview_settings['Sales Order'] = {
    get_indicator: function(doc) {
        // Always show "CANCELLED" in red for cancelled documents
        if (doc.docstatus === 2) {
            return [__("CANCELLED"), "red", "docstatus,=,2"];
        }
        // Fallback to workflow_state or status for non-cancelled documents
        const status = doc.workflow_state || doc.status || "Draft";
        let color = "blue"; // Default color
        if (status === "Submitted") color = "green";
        else if (status === "On Hold") color = "orange";
        // Add other workflow states and colors as needed
        return [__(status), color, `workflow_state,=,${
            status
        }|status,=,${
            status
        }`];
    },

    formatters: {
        // Override workflow_state column to show "CANCELLED" in red
        workflow_state: function(value, df, doc) {
            if (doc.docstatus === 2) {
                return `<span style="color:red; font-weight:bold;">CANCELLED</span>`;
            }
            return value || doc.status || "Draft";
        },
        // Override status column to show "Cancelled" in red
        status: function(value, df, doc) {
            if (doc.docstatus === 2) {
                return `<span style="color:red; font-weight:bold;">Cancelled</span>`;
            }
            return value || doc.workflow_state || "Draft";
        }
    },

    onload: function(listview) {
        // Add a menu item to filter cancelled orders
        listview.page.add_menu_item(__("Show Cancelled"), function() {
            listview.filter_area.clear();
            listview.filter_area.add([[listview.doctype, "docstatus", "=", 2]]);
            listview.refresh();
        }, true);
    }
};