frappe.ui.form.on('Sales Order', {
    before_workflow_action: function(frm, action) {
        // Only block when moving TO "Approved"
        if (frm.doc.workflow_state !== "Dispatched") return;

        return new Promise((resolve, reject) => {
            // Check if Courier Details already exist
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Courier Details",
                    filters: { custom_sales_order: frm.doc.name },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function(r) {
                    frappe.dom.unfreeze();

                    if (!r.message || r.message.length === 0) {
                        // Show dialog to create Courier Details
                        let d = new frappe.ui.Dialog({
                            title: __("Enter Courier Details ( --> Start Transit )"),
                            fields: [
                                { label: "First Name", fieldname: "first_name", fieldtype: "Data", reqd: 1 },
                                { label: "Last Name", fieldname: "last_name", fieldtype: "Data", reqd: 1 },
                                // { label: "Full Name", fieldname: "full_name", fieldtype: "Data", read_only: 1 },
                                { label: "Mobile No.", fieldname: "mobile_no", fieldtype: "Data", reqd: 1 },
                                { label: "Number Of Boxes", fieldname: "number_of_boxes", fieldtype: "Int", reqd: 1 },
                                // { label: "Weight (Kg)", fieldname: "weight_kg", fieldtype: "Int", reqd: 1 },
                                // { label: "Transport (UGX)", fieldname: "transport_ugx", fieldtype: "Currency" },
                                { label: "Dispatch Date", fieldname: "dispatch_date", fieldtype: "Date", reqd: 1 },
                                // { label: "Delivery Note", fieldname: "delivery_note", fieldtype: "Link", options: "Delivery Note" }
                            ],
                            primary_action_label: "Create",
                            primary_action: function(values) {
                                // Auto-fill Full Name
                                values.full_name = values.first_name + " " + values.last_name;

                                // Add linked Sales Order
                                values.custom_sales_order = frm.doc.name;

                                frappe.call({
                                    method: "frappe.client.insert",
                                    args: { doc: Object.assign({ doctype: "Courier Details" }, values) },
                                    callback: function(res) {
                                        frappe.msgprint({
                                            title: __("Created"),
                                            message: __("Courier Details record created successfully."),
                                            indicator: "green"
                                        });
                                        d.hide();
                                        resolve(); // Allow workflow to proceed
                                    },
                                    error: function() {
                                        frappe.msgprint({
                                            title: __("Error"),
                                            message: __("Failed to create Courier Details. Please try again."),
                                            indicator: "red"
                                        });
                                        reject(); // Block workflow
                                    }
                                });
                            }
                        });
                        d.show();

                        // Block workflow until dialog handled
                        reject();
                    } else {
                        // Already exists, proceed
                        resolve();
                    }
                },
                error: function() {
                    frappe.dom.unfreeze();
                    frappe.msgprint({
                        title: __("Error"),
                        message: __("Failed to verify Courier Details. Please try again."),
                        indicator: "red"
                    });
                    reject();
                }
            });
        });
    }
});
