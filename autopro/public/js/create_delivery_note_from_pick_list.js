// frappe.ui.form.on("Pick List", {
//     refresh: function(frm) {
//         if (!frm.doc.__islocal) {
//             frm.add_custom_button(__('Delivery Note'), function() {
//                 frappe.call({
//                     method: "autopro.custom_scripts.create_dn_from_pick_list.create_delivery_note_from_pick_list",
//                     args: { pick_list_name: frm.doc.name },
//                     freeze: true,
//                     freeze_message: "Creating Delivery Note...",
//                     callback: function(r) {
//                         if (r.message) {
//                             frappe.msgprint(`Delivery Note ${r.message.name} created successfully`);
//                             frappe.set_route("Form", r.message.doctype, r.message.name);
//                         }
//                     }
//                 });
//             }, __('Create')); // Makes it a dropdown under "Create"
//         }
//     }
// });
