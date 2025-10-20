frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        // Set up change events
        if (frm.fields_dict.items && frm.fields_dict.items.grid) {
            frm.fields_dict.items.grid.get_field("discount_amount").change = function() {
                calculate_discounts(frm);
            };
            frm.fields_dict.items.grid.get_field("qty").change = function() {
                calculate_discounts(frm);
            };
            frm.fields_dict.items.grid.get_field("rate").change = function() {
                calculate_discounts(frm);
            };
        }
    },
    onload: function(frm) {
        calculate_discounts(frm);
    }
});

frappe.ui.form.on("Sales Order Item", {
    discount_amount: function(frm, cdt, cdn) {
        calculate_discounts(frm);
    },
    qty: function(frm, cdt, cdn) {
        calculate_discounts(frm);
    },
    rate: function(frm, cdt, cdn) {
        calculate_discounts(frm);
    }
});

function calculate_discounts(frm) {
    let total_items_discount = 0;
    let total_net_amount = 0;
    
    // Calculate for each item
    $.each(frm.doc.items || [], function(i, item) {
        const qty = flt(item.qty) || 0;
        const rate = flt(item.rate) || 0;
        const discount = flt(item.discount_amount) || 0;
        
        const base_amount = qty * rate;
        const item_net_amount = base_amount - discount;
        
        total_items_discount += discount;
        total_net_amount += item_net_amount;
        
        // Update item's net amount if different
        if (item.net_amount !== item_net_amount) {
            frappe.model.set_value(cdt, cdn, "net_amount", item_net_amount);
        }
    });
    
    // Use additional_discount_amount if you need to store the total
    if (frm.fields_dict.additional_discount_amount) {
        frm.set_value("additional_discount_amount", total_items_discount);
    }
    
    // These fields definitely exist in standard ERPNext
    frm.set_value("net_total", total_net_amount);
    frm.trigger("calculate_taxes_and_totals");
}