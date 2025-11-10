// frappe.ui.form.on('Sales Order', {
//     before_workflow_action: function(frm, action) {
//         // Only apply to the specific workflow
//         if (frm.doc.workflow !== "Sales Order Credit Approval Revised") {
//             return;
//         }

//         // Only block when moving TO "Dispatched"
//         if (frm.doc.workflow_state !== "Dispatched") {
//             return;
//         }

//         return new Promise((resolve, reject) => {
//             frappe.dom.freeze(__("Verifying Courier Details..."));

//             frappe.call({
//                 method: "frappe.client.get_list",
//                 args: {
//                     doctype: "Courier Details",
//                     filters: { custom_sales_order: frm.doc.name },
//                     fields: ["name"],
//                     limit_page_length: 1
//                 },
//                 callback: function(r) {
//                     frappe.dom.unfreeze();

//                     if (!r.message || r.message.length === 0) {
//                         // No Courier Details → Show dialog
//                         let d = new frappe.ui.Dialog({
//                             title: __("Enter Courier Details → Start Transit"),
//                             fields: [
//                                 { label: "First Name", fieldname: "first_name", fieldtype: "Data", reqd: 1 },
//                                 { label: "Last Name", fieldname: "last_name", fieldtype: "Data", reqd: 1 },
//                                 { label: "Mobile No.", fieldname: "mobile_no", fieldtype: "Data", reqd: 1 },
//                                 { label: "Number Of Boxes", fieldname: "number_of_boxes", fieldtype: "Int", reqd: 1 },
//                                 { label: "Dispatch Date", fieldname: "dispatch_date", fieldtype: "Date", reqd: 1, default: frappe.datetime.nowdate() }
//                             ],
//                             primary_action_label: __("Create & Proceed"),
//                             primary_action: function(values) {
//                                 values.full_name = (values.first_name + " " + values.last_name).trim();
//                                 values.custom_sales_order = frm.doc.name;

//                                 frappe.call({
//                                     method: "frappe.client.insert",
//                                     args: {
//                                         doc: Object.assign({ doctype: "Courier Details" }, values)
//                                     },
//                                     callback: function(res) {
//                                         if (res.message) {
//                                             frappe.msgprint({
//                                                 title: __("Success"),
//                                                 message: __("Courier Details created."),
//                                                 indicator: "green"
//                                             });
//                                             d.hide();
//                                             resolve(); // Allow workflow
//                                         }
//                                     },
//                                     error: function() {
//                                         frappe.msgprint({
//                                             title: __("Error"),
//                                             message: __("Failed to create Courier Details."),
//                                             indicator: "red"
//                                         });
//                                         reject(); // Block
//                                     }
//                                 });
//                             }
//                         });
//                         d.show();
//                         reject(); // Block until dialog completes
//                     } else {
//                         resolve(); // Already exists → Proceed
//                     }
//                 },
//                 error: function() {
//                     frappe.dom.unfreeze();
//                     frappe.msgprint({
//                         title: __("Error"),
//                         message: __("Could not check Courier Details."),
//                         indicator: "red"
//                     });
//                     reject();
//                 }
//             });
//         });
//     }
// });