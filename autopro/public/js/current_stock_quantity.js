frappe.ui.form.on('Sales Order Item', {
    item_code: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code) {
            update_stock_quantity(frm, row);
        } else {
            frappe.model.set_value(cdt, cdn, 'actual_qty', 0);
        }
    },
    warehouse: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.warehouse) {
            update_stock_quantity(frm, row);
        }
    }
});

function update_stock_quantity(frm, row) {
    frappe.call({
        method: 'erpnext.stock.utils.get_stock_balance',
        args: {
            item_code: row.item_code,
            warehouse: row.warehouse || frm.doc.set_source_warehouse,
            company: frm.doc.company
        },
        callback: function (r) {
            frappe.model.set_value(row.doctype, row.name, 'actual_qty', r.message || 0);
        }
    });
}