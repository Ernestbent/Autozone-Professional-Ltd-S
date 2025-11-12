frappe.ui.form.on('Packing List', {
    sales_invoice: function(frm) {
        if (!frm.doc.sales_invoice) return;

        frm.clear_table('table_ttya');

        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Sales Invoice',
                name: frm.doc.sales_invoice
            },
            callback: function(r) {
                if (r.message && r.message.items) {
                    r.message.items.forEach(i => {
                        let row = frm.add_child('table_ttya');
                        row.item_code = i.item_code;
                        row.item_name = i.item_name;
                        row.qty = i.qty;
                        row.uom = i.uom;
                        row.description = i.description;
                        row.rate = i.rate;
                        row.amount = i.amount;
                        row.base_rate = i.base_rate;
                        row.base_amount = i.base_amount;
                        row.income_account = i.income_account;
                        row.cost_center = i.cost_center;
                        row.conversion_factor = i.conversion_factor;
                    });
                    frm.refresh_field('table_ttya');
                }
            }
        });
    }
});