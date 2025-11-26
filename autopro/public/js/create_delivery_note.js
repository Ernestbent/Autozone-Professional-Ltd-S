// frappe.ui.form.on("Sales Order", {
//     before_workflow_action: function(frm) {
//         const action = frm.selected_workflow_action;
        
//         if (action === "Create Delivery Note") {
//             // Return a Promise to control workflow transition
//             return new Promise((resolve, reject) => {
//                 frappe.call({
//                     method: "autopro.custom_scripts.create_delivery_note.create_delivery_note_from_sales_order",
//                     args: { source_name: frm.doc.name },
//                     freeze: true,
//                     freeze_message: __("Creating Delivery Note..."),
//                     callback: function(r) {
//                         frappe.dom.unfreeze(); // Unfreeze after call
                        
//                         if (r.message) {
//                             frappe.msgprint({
//                                 title: __("Success"),
//                                 message: __("Delivery Note created successfully."),
//                                 indicator: "green"
//                             });
                            
//                             // Navigate to the new Delivery Note
//                             frappe.set_route("Form", r.message.doctype, r.message.name);
                            
//                             // ✅ Allow workflow to proceed
//                             resolve();
//                         } else {
//                             frappe.msgprint({
//                                 title: __("Error"),
//                                 message: __("Failed to create Delivery Note."),
//                                 indicator: "red"
//                             });
                            
//                             // ❌ Block workflow transition
//                             reject();
//                         }
//                     },
//                     error: function(err) {
//                         frappe.dom.unfreeze(); // Unfreeze on error
                        
//                         frappe.msgprint({
//                             title: __("Request Failed"),
//                             message: __("Delivery Note already exists for this Sales Order."),
//                             indicator: "red"
//                         });
//                         console.error(err);
                        
//                         // ❌ Block workflow transition - this prevents state change
//                         reject();
//                     }
//                 });
//             });
//         }
//     }
// });