// frappe.ui.form.on("Delivery Note", {
//     refresh: function(frm) {
        
//         // Only show the button if gate pass fields are empty
//         if (!frm.doc.custom_office_gate_pass && !frm.doc.custom_store_gate_pass) {
//             frm.add_custom_button(__("Generate Gate Passes"), function() {
//                 frappe.call({
//                     method: "autopro.custom_scripts.get_gate_and_office_pass.generate_gate_pass",
//                     args: {}, 
//                     callback: function(r) {
//                         if (r.message) {
//                             // Update form fields with generated gate pass numbers
//                             frm.set_value("custom_office_gate_pass", r.message.custom_office_gate_pass);
//                             frm.set_value("custom_store_gate_pass", r.message.custom_store_gate_pass);
//                             frm.refresh(); // Refresh form to reflect changes and hide button
//                             frappe.msgprint(__("Success"));
//                         }
//                     },
//                     error: function(r) {
//                         frappe.msgprint({
//                             title: __("Error"),
//                             indicator: "red",
//                             message: __("Failed to generate gate passes: {0}", [r.exc || "Unknown error"])
//                         });
//                     }
//                 });
//             });
//         }
//     },
//     custom_office_gate_pass: function(frm) {
//         // Refresh the form when custom_office_gate_pass changes to update button visibility
//         frm.refresh();
//     },
//     custom_store_gate_pass: function(frm) {
//         // Refresh the form when custom_store_gate_pass changes to update button visibility
//         frm.refresh();
//     }
// });