frappe.listview_settings['Sales Order'] = {
    add_fields: ['sales_team.sales_person'], // Force column to appear
    get_indicator: function(doc) { /* ... */ }
};