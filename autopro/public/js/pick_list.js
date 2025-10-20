frappe.ui.form.on('Pick List', {
    refresh: function(frm) {
        // Add custom button or trigger initial calculation
    }
});

frappe.ui.form.on('Pick List Item', {
    item_code: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code) {
            update_stock_quantity(frm, row, cdt, cdn);
        }
    },
    warehouse: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code && row.warehouse) {
            update_stock_quantity(frm, row, cdt, cdn);
        }
    }
});

function update_stock_quantity(frm, row, cdt, cdn) {
    if (!row.warehouse) {
        // If warehouse is not set, use parent's source warehouse
        row.warehouse = frm.doc.set_warehouse;
    }
    
    if (!row.warehouse || !row.item_code) return;
    
    frappe.call({
        method: 'erpnext.stock.utils.get_stock_balance',
        args: {
            item_code: row.item_code,
            warehouse: row.warehouse,
            company: frm.doc.company
        },
        callback: function (r) {
            let qty_available = r.message || 0;
            
            // Try different possible field names
            const possible_fields = ['actual_qty', 'stock_qty', 'qty_available', 'available_qty'];
            
            for (let field of possible_fields) {
                if (frappe.meta.has_field(cdt, field)) {
                    frappe.model.set_value(cdt, cdn, field, qty_available);
                    return;
                }
            }
            
            // If no field exists, show alert and set in stock_qty (common in Pick List)
            frappe.model.set_value(cdt, cdn, 'stock_qty', qty_available);
            
            frappe.show_alert({
                message: `Available Quantity for ${row.item_code}: ${qty_available}`,
                indicator: 'blue'
            }, 3);
        }
    });
}