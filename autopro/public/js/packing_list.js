frappe.ui.form.on("Packing Slip", {
    refresh: function(frm) {
        if (frm.doc.delivery_note && frm.doc.items.length) {
            frm.doc.items.forEach(function(row) {
                if (!row.custom_rate && !row.custom_amount) {
                    frappe.call({
                        method: "autopro.custom_scripts.packing_list.fetch_delivery_note_items",
                        args: { delivery_note: frm.doc.delivery_note },
                        callback: function(r) {
                            if (r.message) {
                                r.message.forEach(function(d) {
                                    let item_row = frm.doc.items.find(i => i.item_code === d.item_code);
                                    if(item_row){
                                        frappe.model.set_value(item_row.doctype, item_row.name, "custom_rate", d.custom_rate);
                                        frappe.model.set_value(item_row.doctype, item_row.name, "custom_amount", d.custom_amount);
                                    }
                                });
                            }
                        }
                    });
                }
            });
        }
    }
});
