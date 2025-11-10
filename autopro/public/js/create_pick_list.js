frappe.ui.form.on("Sales Order", {
    before_workflow_action: function(frm) {
        const action = frm.selected_workflow_action;

        if(action === "Create Pick List") {
            frappe.validated = false;

            frappe.call({
                method: "autopro.custom_scripts.create_pick_list.create_pick_list_from_sales_order", 
                args: { source_name: frm.doc.name },
                freeze: true,
                freeze_message: "Creating Pick List...",
                callback: function(r) {
                    if(r.message) {
                        frappe.set_route("Form", r.message.doctype, r.message.name);
                    } else {
                        frappe.msgprint({
                            title: __("Error"),
                            message: "Failed to create Pick List",
                            indicator: "red"
                        });
                    }
                },
                error: function(err) {
                    frappe.msgprint({
                        title: __("Request Failed"),
                        message: "Could not process Create Pick List",
                        indicator: "red"
                    });
                    console.error(err);
                }
            });
        }
    }
});
