frappe.ui.form.on('Sales Invoice Item', {
    discount_amount: function(frm, cdt, cdn) {
        var item = frappe.get_doc(cdt, cdn);
        if (item.discount_amount && !item.discount_account) {
            frappe.model.set_value(cdt, cdn, 'discount_account', 'Discount Allowed - APL');
        }
    }
});