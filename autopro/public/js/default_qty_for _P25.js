// Function to enforce multiples of 25
function enforceMultipleOf25(frm, row) {
    if (row.qty && row.qty > 0) {
        // Calculate nearest multiple of 25 (rounding UP)
        let multiple = Math.ceil(row.qty / 25) * 25;
        
        // Only adjust and show message if not already a multiple of 25
        if (row.qty !== multiple) {
            let message = __("Quantity must be in multiples of 25. Adjusted from {0} to {1} pieces for item {2}", [row.qty, multiple, row.item_name]);
            console.log('Adjusting:', message);
            
            frappe.show_alert({
                message: message,
                indicator: 'blue'
            }, 5);
            
            // Set the value directly
            frappe.model.set_value(row.doctype, row.name, 'qty', multiple);
        }
    }
}

// Event handler for Sales Order Item quantity changes
frappe.ui.form.on("Sales Order Item", {
    qty: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.item_name && row.item_name.endsWith('-P25')) {
            console.log('Qty changed for P25 item:', row.item_name, 'qty:', row.qty);
            enforceMultipleOf25(frm, row);
        }
    }
});

// Event handler for Sales Order form
frappe.ui.form.on("Sales Order", {
    before_save: function(frm) {
        console.log('before_save event triggered');
        // Double-check all rows before saving
        let items = frm.doc.items || [];
        for (let i = 0; i < items.length; i++) {
            let row = items[i];
            if (row.item_name && row.item_name.endsWith('-P25')) {
                console.log('Final check before save:', row.item_name, 'qty:', row.qty);
                enforceMultipleOf25(frm, row);
            }
        }
    }
});