// frappe.ui.form.on('Sales Order', {
//     before_workflow_action: function(frm) {
//         const next_action = frm.selected_workflow_action;
//         const next_state = frm.doc.workflow_state;

//         // Only apply to "Start Transit" action (Dispatched → In Transit)
//         if (next_action !== "Start Transit") return;

//         return new Promise((resolve, reject) => {
//             // First, check if the active workflow is "Sales Order Credit Approval Revised"
//             frappe.call({
//                 method: "frappe.client.get_value",
//                 args: {
//                     doctype: "Workflow",
//                     filters: {
//                         document_type: "Sales Order",
//                         is_active: 1,
//                         name: "Sales Order Credit Approval Revised"
//                     },
//                     fieldname: ["name"]
//                 },
//                 callback: function(workflow_check) {
//                     // If this workflow is not active, just resolve and continue
//                     if (!workflow_check.message) {
//                         resolve();
//                         return;
//                     }
                    
//                     // Workflow is active, proceed with courier details check
//                     frappe.call({
//                         method: "frappe.client.get_list",
//                         args: {
//                             doctype: "Courier Details",
//                             filters: { custom_sales_order: frm.doc.name },
//                             fields: ["name"],
//                             limit_page_length: 1
//                         },
//                         freeze: true,
//                         freeze_message: __("Verifying Courier Details..."),
//                         callback: function(r) {
//                             // ⚡ IMPORTANT: Unfreeze the screen before showing dialog
//                             frappe.dom.unfreeze();
                            
//                             if (!r.message || r.message.length === 0) {
//                                 // No Courier Details → Show dialog
//                                 const d = new frappe.ui.Dialog({
//                                     title: __("Enter Courier Details → Start Transit"),
//                                     fields: [
//                                         { label: "First Name", fieldname: "first_name", fieldtype: "Data", reqd: 1 },
//                                         { label: "Last Name", fieldname: "last_name", fieldtype: "Data", reqd: 1 },
//                                         { label: "Mobile No.", fieldname: "mobile_no", fieldtype: "Data", reqd: 1 },
//                                         { label: "Number Of Boxes", fieldname: "number_of_boxes", fieldtype: "Int", reqd: 1 },
//                                         { label: "Weight (Kg)", fieldname: "weight_kg", fieldtype: "Int", reqd: 1 },
//                                         { label: "Dispatch Date", fieldname: "dispatch_date", fieldtype: "Date", reqd: 1, default: frappe.datetime.nowdate() }
//                                     ],
//                                     primary_action_label: __("Create & Proceed"),
//                                     primary_action(values) {
//                                         // Validate required fields
//                                         if (!values.first_name || !values.last_name || !values.mobile_no || !values.number_of_boxes || !values.weight_kg || !values.dispatch_date) {
//                                             frappe.msgprint({
//                                                 title: __("Required"),
//                                                 indicator: "red",
//                                                 message: __("Please fill all required fields before continuing.")
//                                             });
//                                             return;
//                                         }
                                        
//                                         values.full_name = `${values.first_name} ${values.last_name}`.trim();
//                                         values.custom_sales_order = frm.doc.name;

//                                         // Disable button during call
//                                         d.get_primary_btn().attr("disabled", true);

//                                         frappe.call({
//                                             method: "frappe.client.insert",
//                                             args: { doc: Object.assign({ doctype: "Courier Details" }, values) },
//                                             freeze: true,
//                                             freeze_message: __("Saving Courier Details..."),
//                                             callback(res) {
//                                                 frappe.dom.unfreeze(); // Unfreeze after call
//                                                 d.get_primary_btn().attr("disabled", false);
                                                
//                                                 if (res.message) {
//                                                     frappe.msgprint({
//                                                         title: __("Success"),
//                                                         message: __("Courier Details created successfully."),
//                                                         indicator: "green"
//                                                     });
//                                                     d.hide();
                                                    
//                                                     // ✅ Allow workflow to proceed
//                                                     resolve();
//                                                 } else {
//                                                     frappe.msgprint({
//                                                         title: __("Error"),
//                                                         message: __("Could not create Courier Details."),
//                                                         indicator: "red"
//                                                     });
                                                    
//                                                     // Block workflow transition
//                                                     reject();
//                                                 }
//                                             },
//                                             error() {
//                                                 frappe.dom.unfreeze(); // Unfreeze on error
//                                                 d.get_primary_btn().attr("disabled", false);
                                                
//                                                 frappe.msgprint({
//                                                     title: __("Error"),
//                                                     message: __("Failed to create Courier Details."),
//                                                     indicator: "red"
//                                                 });
                                                
//                                                 // Block workflow transition
//                                                 reject();
//                                             }
//                                         });
//                                     },
//                                     secondary_action_label: __("Cancel"),
//                                     secondary_action() {
//                                         d.hide();
//                                         frappe.msgprint({
//                                             title: __("Cancelled"),
//                                             indicator: "orange",
//                                             message: __("Workflow transition cancelled.")
//                                         });
                                        
//                                         // Block workflow transition
//                                         reject();
//                                     }
//                                 });
                                
//                                 d.show();
//                             } else {
//                                 // Courier details exist → proceed normally
//                                 resolve();
//                             }
//                         },
//                         error: function() {
//                             frappe.dom.unfreeze(); // Unfreeze on error
                            
//                             frappe.msgprint({
//                                 title: __("Error"),
//                                 message: __("Could not check Courier Details."),
//                                 indicator: "red"
//                             });
                            
//                             // Block workflow transition
//                             reject();
//                         }
//                     });
//                 },
//                 error: function() {
//                     // If workflow check fails, just proceed
//                     resolve();
//                 }
//             });
//         });
//     }
// });