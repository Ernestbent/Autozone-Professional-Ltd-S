// frappe.ui.form.on("Sales Order", {
//     before_workflow_action: function (frm) {
//         // Log for debugging
//         console.log("Workflow action triggered:", frm.selected_workflow_action, "Current state:", frm.doc.workflow_state);
        
//         // Check if the action is "Deliver" or the target state is "Delivered"
//         if (frm.selected_workflow_action === "Mark As Delivered" || frm.doc.workflow_state === "Delivered") {
            
//             // Return a Promise to control workflow transition
//             return new Promise((resolve, reject) => {
                
//                 // ⚡ IMPORTANT: Unfreeze the screen before showing dialog
//                 frappe.dom.unfreeze();
                
//                 let d = new frappe.ui.Dialog({
//                     title: "Update Delivery Note Received Date",
//                     fields: [
//                         {
//                             label: "Received Date",
//                             fieldname: "delivery_date",
//                             fieldtype: "Date",
//                             reqd: 1,
//                             default: frappe.datetime.get_today() // Optional: Set today as default
//                         }
//                     ],
//                     primary_action_label: "Update & Continue",
//                     primary_action(values) {
//                         // Validate that date is entered
//                         if (!values.delivery_date) {
//                             frappe.msgprint({
//                                 title: __("Required"),
//                                 indicator: "red",
//                                 message: __("Please select a delivery date before continuing.")
//                             });
//                             return; // Don't proceed if no date
//                         }
                        
//                         // Disable button during call
//                         d.get_primary_btn().attr("disabled", true);
                        
//                         frappe.call({
//                             method: "autopro.custom_scripts.update_dn_date.update_delivery_date",
//                             args: {
//                                 sales_order: frm.doc.name,
//                                 delivery_date: values.delivery_date
//                             },
//                             freeze: true, // Freeze during the call
//                             freeze_message: __("Updating Delivery Date..."),
//                             callback: function (r) {
//                                 frappe.dom.unfreeze(); // Unfreeze after call
//                                 d.get_primary_btn().attr("disabled", false);
                                
//                                 if (!r.exc) {
//                                     frappe.msgprint({
//                                         title: "Success",
//                                         indicator: "green",
//                                         message: `Updated Delivery Notes: ${r.message.join(", ") || "None"}`
//                                     });
                                    
//                                     d.hide();
                                    
//                                     // ✅ Allow workflow to proceed
//                                     resolve();
                                    
//                                 } else {
//                                     frappe.msgprint({
//                                         title: "Error",
//                                         indicator: "red",
//                                         message: `Failed to update Delivery Notes: ${r.exc || "Unknown server error"}.`
//                                     });
//                                     console.error("Server error response:", r);
                                    
//                                     // ❌ Block workflow transition
//                                     reject();
//                                 }
//                             },
//                             error: function (err) {
//                                 frappe.dom.unfreeze(); // Unfreeze on error
//                                 d.get_primary_btn().attr("disabled", false);
                                
//                                 frappe.msgprint({
//                                     title: "Error",
//                                     indicator: "red",
//                                     message: `An error occurred: ${err.message || "Unknown error"}.`
//                                 });
//                                 console.error("Client-side error details:", err);
                                
//                                 // ❌ Block workflow transition
//                                 reject();
//                             }
//                         });
//                     },
//                     secondary_action_label: "Cancel",
//                     secondary_action() {
//                         d.hide();
//                         frappe.msgprint({
//                             title: __("Cancelled"),
//                             indicator: "orange",
//                             message: __("Workflow transition cancelled.")
//                         });
                        
//                         // ❌ Block workflow transition
//                         reject();
//                     }
//                 });
                
//                 d.show();
//             });
//         }
//     }
// });