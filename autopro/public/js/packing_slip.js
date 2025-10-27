frappe.ui.form.on('Packing Slip', {
    refresh(frm) {
        calculate_totals(frm);
    }
});

frappe.ui.form.on('Packing Slip Box', {
    quantity(frm, cdt, cdn) {
        calculate_totals(frm);
    },
    weight_of_box(frm, cdt, cdn) {
        calculate_totals(frm);
    },
    expense_of_box(frm, cdt, cdn) {
        calculate_totals(frm);
    },
    items_add(frm, cdt, cdn) {
        calculate_totals(frm);
    },
    items_remove(frm, cdt, cdn) {
        calculate_totals(frm);
    }
});

function calculate_totals(frm) {
    let total_qty = 0;
    let total_weight = 0;
    let total_expense = 0;

    frm.doc.custom_box_details.forEach(row => {
        total_qty += row.quantity || 0;
        total_weight += parseFloat(row.weight_of_box || 0);
        total_expense += parseFloat(row.expense_of_box || 0);
    });

    // Update totals in main form
    frm.set_value('custom_total_qty', total_qty);
    frm.set_value('custom_weight', total_weight);
    frm.set_value('custom_billed_amount', total_expense);
    frm.set_value('custom_number_of_boxes', frm.doc.custom_box_details.length); // number of boxes

    frm.refresh_field('custom_total_qty');
    frm.refresh_field('custom_weight');
    frm.refresh_field('custom_billed_amount');
    frm.refresh_field('custom_number_of_boxes');

    // Validate total quantity against Delivery Note
    let dn_total_qty = 0;
    frm.doc.items.forEach(item => {
        dn_total_qty += item.qty || 0;
    });

    if (total_qty > dn_total_qty) {
        frappe.msgprint({
            title: __('Quantity Exceeded'),
            message: __('Total quantity in packing boxes exceeds the total quantity in Delivery Note.'),
            indicator: 'red'
        });
        frappe.validated = false; // prevent saving
    }
}
