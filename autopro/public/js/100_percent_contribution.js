frappe.ui.form.on('Customer', {
    refresh: function(frm) {
        // Clear existing Sales Team table to avoid conflicts
        if (!frm.doc.sales_team || frm.doc.sales_team.length === 0) {
            // Add a single row with default sales person
            frappe.db.get_value('Sales Person', {'company': 'APL', 'is_active': 1}, 'name', (result) => {
                if (result && result.name) {
                    let row = frm.add_child('sales_team');
                    row.sales_person = result.name;
                    row.allocated_percentage = 100; // Default to 100, but not enforced
                    frm.refresh_field('sales_team');
                } else {
                    frappe.msgprint({
                        title: __('Warning'),
                        indicator: 'orange',
                        message: __('No active Sales Person found for company APL. Please create one in Sales Person list.')
                    });
                }
            });
        }
    },
    sales_team: function(frm) {
        // Allow any number of rows or percentages without validation
        if (frm.doc.sales_team && frm.doc.sales_team.length > 0) {
            // Optionally set first row to 100% if desired
            frm.doc.sales_team[0].allocated_percentage = 100;
            frm.refresh_field('sales_team');
        }
    }
});