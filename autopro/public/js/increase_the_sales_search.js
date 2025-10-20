frappe.ui.form.on('Sales Order Item', {
    item_code: function(frm, cdt, cdn) {
        // Optional: you can reload suggestions on item_code change
    }
});

frappe.ui.form.on('Sales Order', {
    onload: function(frm) {
        frm.fields_dict.items.grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
            return {
                query: "erpnext.controllers.queries.item_query",
                filters: {
                    'is_sales_item': 1
                },
                page_length: 100  // 👈 This increases the number of items shown
            };
        };
    }
});
