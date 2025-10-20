frappe.ui.form.on('Sales Order', {
    customer: function(frm) {
        if (frm.doc.customer && frm.doc.company) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'GL Entry',
                    fields: ['sum(debit - credit) as balance'],
                    filters: {
                        'party_type': 'Customer',
                        'party': frm.doc.customer,
                        'company': frm.doc.company,
                        'is_cancelled': 0
                    }
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        frm.set_value('custom_current_outstanding', r.message[0].balance || 0);
                    }
                }
            });
        } else {
            frm.set_value('custom_current_outstanding', 0);
        }
    }
});
