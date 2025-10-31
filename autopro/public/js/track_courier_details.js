frappe.ui.form.on("Sales Order", {
    before_workflow_action: function (frm) {
        if (frm.selected_workflow_action === "Start Transit") {
            frappe.validated = false; // Block the initial transition

            const d = new frappe.ui.Dialog({
                title: "Enter Courier Details",
                fields: [
                    { label: "First Name", fieldname: "first_name", fieldtype: "Data", reqd: 1 },
                    { label: "Last Name", fieldname: "last_name", fieldtype: "Data", reqd: 1 },
                    { label: "Mobile No.", fieldname: "mobile_no", fieldtype: "Data", reqd: 1 },
                    { label: "Vehicle Number", fieldname: "vehicle_number", fieldtype: "Data" },
                    { label: "Number Of Boxes", fieldname: "number_of_boxes", fieldtype: "Int", reqd: 1 },
                    { label: "Weight (Kg)", fieldname: "weight_kg", fieldtype: "Int", reqd: 1 },
                    { label: "Dispatch Date", fieldname: "dispatch_date", fieldtype: "Date", reqd: 1 }
                ],
                primary_action_label: "Save & Continue",
                primary_action(values) {
                    d.get_primary_btn().attr("disabled", true);

                    values.full_name = `${values.first_name} ${values.last_name}`;

                    // Save courier details first
                    frappe.call({
                        method: "frappe.client.insert",
                        args: {
                            doc: {
                                doctype: "Courier Details",
                                custom_sales_order: frm.doc.name,
                                first_name: values.first_name,
                                last_name: values.last_name,
                                full_name: values.full_name,
                                mobile_no: values.mobile_no,
                                vehicle_number: values.vehicle_number,
                                number_of_boxes: values.number_of_boxes,
                                weight_kg: values.weight_kg,
                                dispatch_date: values.dispatch_date
                            }
                        },
                        callback: function (r) {
                            if (!r.exc) {
                                frappe.show_alert({ message: "Courier Details Saved", indicator: "green" });
                                d.hide();

                                // Set validated to true and proceed with workflow
                                frappe.validated = true;
                                
                                // Use a server-side method to apply workflow
                                frappe.call({
                                    method: "frappe.client.set_value",
                                    args: {
                                        doctype: "Sales Order",
                                        name: frm.doc.name,
                                        fieldname: "workflow_state",
                                        value: "In Transit" // Replace with your actual next state name
                                    },
                                    callback: function() {
                                        frm.reload_doc();
                                    }
                                });
                            } else {
                                frappe.msgprint("Error saving courier details. Workflow not continued.");
                                d.get_primary_btn().attr("disabled", false);
                            }
                        }
                    });
                }
            });

            d.show();
        }
    }
});