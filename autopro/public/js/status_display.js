frappe.provide("frappe.listview_settings");

// Function to apply listview settings
function applySalesOrderListViewSettings() {
    frappe.listview_settings['Sales Order'] = {
        add_fields: ["docstatus", "status", "workflow_state"],
        onload: function(listview) {
            console.log("Sales Order listview loaded and initialized");
        },
        get_indicator: function(doc) {
            let status = "";

            if (doc.status === "Cancelled" || doc.status === "Closed" || doc.status === "On Hold") {
                status = doc.status;
            } else if (doc.docstatus === 2) {
                status = "Cancelled";
            } else if (doc.docstatus === 1) {
                status = doc.workflow_state || doc.status;
            } else {
                status = "Draft";
            }

            if (status === "Cancelled") {
                return [__(status), "inverse black", "status,=,Cancelled"];
            } else if (status === "Closed") {
                return [__(status), "inverse black", "status,=,Closed"];
            } else if (status === "On Hold") {
                return [__(status), "inverse black", "status,=,On Hold"];
            } else if (status === "Approved") {
                return [__(status), "green", "workflow_state,=,Approved"];
            } else if (status === "Being Delivered") {
                return [__(status), "dark blue", "workflow_state,=,Being Delivered"];
            } else if (status === "Pending Credit Approval") {
                return [__(status), "red", "workflow_state,=,Pending Credit Approval"];
            } else if (status === "Draft") {
                return [__(status), "grey", "docstatus,=,0"];
            } else {
                return [__(status), "blue", "docstatus,=,1"];
            }
        }
    };
}

// Apply settings immediately
applySalesOrderListViewSettings();

// Re-apply on route change (for back/forward navigation)
frappe.router.on('change', function() {
    var route = frappe.get_route();
    if (route[0] === 'List' && route[1] === 'Sales Order') {
        setTimeout(function() {
            applySalesOrderListViewSettings();
            if (cur_list && cur_list.doctype === 'Sales Order') {
                cur_list.refresh();
            }
        }, 100);
    }
});

// Also handle pageshow event for browser navigation
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        var route = frappe.get_route();
        if (route[0] === 'List' && route[1] === 'Sales Order') {
            setTimeout(function() {
                applySalesOrderListViewSettings();
                if (cur_list && cur_list.doctype === 'Sales Order') {
                    cur_list.refresh();
                }
            }, 200);
        }
    }
});