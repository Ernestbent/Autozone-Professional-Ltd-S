frappe.ui.form.on("Payment Entry", {
    mode_of_payment: function(frm) {
        if (frm.doc.mode_of_payment === "Cash") {
            // Set fixed reference number
            frm.set_value("reference_no", "N/A");
            // Make the field read-only
            frm.set_df_property("reference_no", "read_only", 1);
        } else {
            // Enable editing if switching to another mode
            frm.set_df_property("reference_no", "read_only", 0);
            // Optional: clear the fixed value if it was "00000"
            if (frm.doc.reference_no === "N/A") {
                frm.set_value("reference_no", "");
            }
        }
    }
});
