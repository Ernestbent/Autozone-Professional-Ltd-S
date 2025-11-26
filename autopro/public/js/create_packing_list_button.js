frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // Only show button for submitted Sales Orders
        if (frm.doc.docstatus === 1) {
            let buttonName = "Create Packing List";
            let groupName = "Create"; // Under the standard Create button

            frm.add_custom_button(__(buttonName), function() {
                // Action placeholder for now
                frappe.msgprint(__('Button clicked: {0}', [buttonName]));
            }, __(groupName));
        }
    }
});
