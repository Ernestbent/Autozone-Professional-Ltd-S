frappe.query_reports["General Ledger"] = {
    onload: function(report) {
        // Set default value when report loads
        report.set_filter_value('ignore_system_generated_credit_debit_notes', 1);
    }
};