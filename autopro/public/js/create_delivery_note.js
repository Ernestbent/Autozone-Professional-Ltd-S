frappe.ui.form.on("Sales Order", {
    before_workflow_action: function(frm) {
        const action = frm.selected_workflow_action;

        if(action === "Create Delivery Note") {
            frappe.validated = false;

            frappe.call({
                method: "autopro.custom_scripts.create_delivery_note.create_delivery_note_from_sales_order", 
                args: { source_name: frm.doc.name },
                freeze: true,
                freeze_message: "Creating Delivery Note...",
                callback: function(r) {
                    if(r.message) {
                        frappe.set_route("Form", r.message.doctype, r.message.name);
                    } else {
                        frappe.msgprint({
                            title: __("Error"),
                            message: "Failed to create Delivery Note",
                            indicator: "red"
                        });
                    }
                },
                error: function(err) {
                    frappe.msgprint({
                        title: __("Request Failed"),
                        message: "Could not process Create Delivery Note",
                        indicator: "red"
                    });
                    console.error(err);
                }
            });
        }
    }
});