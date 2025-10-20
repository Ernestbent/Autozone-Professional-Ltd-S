frappe.ui.form.on('Sales Order Item', {
    setup: function(frm) {
        // Add discount field to the quick entry form
        frm.fields_dict.item_code.get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    'is_sales_item': 1
                }
            };
        };
    },
    
    before_load: function(frm) {
        // Ensure discount field is in the form
        if (!frm.fields_dict.discount_percentage) {
            frm.add_field('discount_percentage', 'Discount %', 'Percent');
            frm.add_field('discount_amount', 'Discount Amount', 'Currency');
            frm.set_df_property('discount_amount', 'read_only', 1);
        }
    },
    
    discount_percentage: function(frm) {
        // Auto-calculate discount amount
        if (frm.doc.discount_percentage && frm.doc.rate && frm.doc.qty) {
            frm.doc.discount_amount = flt(frm.doc.rate) * flt(frm.doc.qty) * flt(frm.doc.discount_percentage) / 100;
            frm.refresh_field('discount_amount');
        }
    }
});