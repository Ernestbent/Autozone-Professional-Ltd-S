frappe.ui.form.on("Payment Entry", {
    reference_no: function(frm) {
        if (frm.doc.mode_of_payment === "mobile money" && frm.doc.reference_no) {
            frappe.db.get_list("Payment Entry", {
                fields: ["name"],
                filters: {
                    reference_no: frm.doc.reference_no,
                    mode_of_payment: "mobile money",
                    docstatus: ["<", 2]
                },
                limit: 1
            }).then(records => {
                if (records.length && records[0].name !== frm.doc.name) {
                    frappe.msgprint({
                        title: "Duplicate Reference No",
                        message: `Reference Number <b>${frm.doc.reference_no}</b> is already used in Payment Entry <b>${records[0].name}</b>.`,
                        indicator: "red"
                    });
                    frm.set_value("reference_no", "");
                }
            });
        }
    }
});
