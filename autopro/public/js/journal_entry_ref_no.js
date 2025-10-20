frappe.ui.form.on("Journal Entry", {
    onload: function(frm) {
        // Set Reference No to "N/A" if it's empty
        if (!frm.doc.reference_no) {
            frm.set_value("cheque_no", "N/A");
        }
        // Make the field read-only
        frm.set_df_property("cheque_no", "read_only", 1);
    },
    refresh: function(frm) {
        // Always enforce read-only and N/A
        frm.set_value("cheque_no", "N/A");
        frm.set_df_property("cheque_no", "read_only", 1);
    }
});
