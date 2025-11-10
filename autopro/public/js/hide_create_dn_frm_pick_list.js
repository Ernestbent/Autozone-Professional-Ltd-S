frappe.ui.form.on('Pick List', {
    refresh(frm) {
        setTimeout(() => {
            frm.remove_custom_button('Create Delivery Note', 'Create');
            // frm.remove_custom_button('Close', 'Status');
            // frm.remove_custom_button('Work Order', 'Make');
        }, 10);
    }
});
