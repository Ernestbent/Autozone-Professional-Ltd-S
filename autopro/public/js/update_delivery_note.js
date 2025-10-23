frappe.ui.form.on("Sales Order", {
    before_workflow_action: function (frm) {
        // Log for debugging
        console.log("Workflow action triggered:", frm.selected_workflow_action, "Current state:", frm.doc.workflow_state);

        // Check if the action is "Deliver" or the target state is "Delivered"
        if (frm.selected_workflow_action === "Deliver" || frm.doc.workflow_state === "Delivered") {
            frappe.validated = false;

            let d = new frappe.ui.Dialog({
                title: "Update Delivery Note Received Date",
                fields: [
                    {
                        label: "Received Date",
                        fieldname: "delivery_date",
                        fieldtype: "Date",
                        reqd: 1
                    }
                ],
                primary_action_label: "Update & Continue",
                primary_action(values) {
                    d.get_primary_btn().attr("disabled", true); // Disable button during call
                    frappe.call({
                        method: "autopro.custom_scripts.update_dn_date.update_delivery_date",
                        args: {
                            sales_order: frm.doc.name,
                            delivery_date: values.delivery_date
                        },
                        callback: function (r) {
                            d.get_primary_btn().attr("disabled", false); // Re-enable button
                            if (!r.exc) {
                                frappe.msgprint({
                                    title: "Success",
                                    indicator: "green",
                                    message: `Updated Delivery Notes: ${r.message.join(", ") || "None"}`
                                });
                                d.hide();
                                frappe.validated = true;
                                frm.save();
                            } else {
                                // Keep frappe.validated = false to prevent workflow transition
                                frappe.msgprint({
                                    title: "Error",
                                    indicator: "red",
                                    message: `Failed to update Delivery Notes: ${r.exc || "Unknown server error"}. The workflow transition has been halted. Please check the input or contact support.`
                                });

                                // Log full response for debugging
                                console.error("Server error response:", r);
                            }
                        },
                        error: function (err) {
                            d.get_primary_btn().attr("disabled", false); 
                            // Keep frappe.validated = false to prevent workflow transition
                            frappe.msgprint({
                                title: "Error",
                                indicator: "red",
                                message: `An error occurred during the request: ${err.message || JSON.stringify(err) || "Unknown error"}. The workflow transition has been halted. Please check your network connection or contact support.`
                            });
                            // Log full error object for debugging
                            console.error("Client-side error details:", err);
                        }
                    });
                }
            });

            d.show();
        }
    }
});