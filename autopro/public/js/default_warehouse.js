frappe.ui.form.on("Sales Order", {
    onload: function(frm) {
        // Set default warehouse only for new documents
        if (frm.is_new() && !frm.doc.set_warehouse) {
            frm.set_value("set_warehouse", "Main Loc - APL");
        }
    }
});