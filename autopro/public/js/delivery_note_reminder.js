frappe.ui.form.on('Packing Slip', {
    on_submit: function(frm) {
        // Check if a Delivery Note is linked
        if(frm.doc.delivery_note) {
            // Fetch the Delivery Note document
            frappe.db.get_doc('Delivery Note', frm.doc.delivery_note).then(doc => {
                // If Delivery Note is still Draft
                if(doc.docstatus === 0) {
                    let d = new frappe.ui.Dialog({
                        title: __("Delivery Note Not Submitted Yet"),
                        fields: [
                            {fieldname: 'info', fieldtype: 'HTML', options: `The Delivery Note <b>${doc.name}</b> is still Draft.`}
                        ],
                        primary_action_label: 'Open Delivery Note',
                        primary_action() {
                            frappe.set_route('Form', 'Delivery Note', doc.name);
                            d.hide();
                        }
                    });
                    d.show();

                    // Optionally, stop the submission
                    frappe.validated = false;
                }
            });
        }
    }
});
