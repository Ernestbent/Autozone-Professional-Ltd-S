frappe.ui.form.on('Sales Order', {
    before_workflow_action: function(frm) {
        if (frm.selected_workflow_action === "Create Packing List") {

            // Block immediate transition
            frm.selected_workflow_action = null;

            frappe.call({
                method: "autopro.custom_scripts.create_packing_list.create_packing_list_from_sales_order",
                args: { source_name: frm.doc.name },
                callback: function(r) {
                    if (r && r.message) {
                        const pl_name = r.message.name;

                        // Open the Packing List
                        frappe.set_route("Form", "Packing List", pl_name);

                        // When the Packing List is SUBMITTED → move SO to "Completed"
                        const handler = function(data) {
                            if (data.doctype === "Packing List" && 
                                data.name === pl_name && 
                                data.docstatus === 1) {  // Submitted

                                // Only if still in "Delivered"
                                if (frm.doc.workflow_state === "Delivered") {
                                    frappe.db.set_value("Sales Order", frm.doc.name, "workflow_state", "Completed")
                                        .then(() => {
                                            frm.reload_doc();
                                            // frappe.show_alert({
                                            //     message: __("Packing List submitted  Sales Order is now Completed"),
                                            //     indicator: "green"
                                            // }, 5);
                                        });
                                }

                                // Clean up the listener
                                frappe.realtime.off("doc_update", handler);
                            }
                        };

                        frappe.realtime.on("doc_update", handler);
                    }
                }
            });

            // Stop the transition
            return false;
        }
    }
});