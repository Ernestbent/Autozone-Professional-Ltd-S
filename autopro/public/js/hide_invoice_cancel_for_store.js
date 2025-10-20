frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
        const allowed_users = [
            'dministrator',
            'accounts@autozonepro.org',
            'warehouse@autozonepro.org',
            'finance@autozonepro.org',
            'reports@autozonepro.org',
            'audit@autozonepro.org'
        ];

        // Check if the document is submitted and the user is not allowed
        if (frm.doc.docstatus === 1 && !allowed_users.includes(frappe.session.user)) {
            // Remove the Cancel button from the Actions menu
            frm.remove_custom_button('Cancel', 'Actions');

            // Remove the Cancel button from the inner button group
            frm.page.remove_inner_button('Cancel', 'Actions');

            // Handle dynamic rendering with a slight delay
            setTimeout(() => {
                // Hide the Cancel button if it is the primary action
                if (frm.page.btn_primary && frm.page.btn_primary.text() === 'Cancel') {
                    frm.page.btn_primary.hide();
                }

                // Hide the Cancel option in the dropdown menu
                frm.page.menu.find('a:contains("Cancel"), a:contains("CANCEL"), a:contains("cancel")').parent().hide();
            }, 1);
        }
    }
});