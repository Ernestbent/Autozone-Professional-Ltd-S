frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        frm.set_query('customer', function() {
            return {
                query: 'frappe.desk.search.search_link',
                filters: { doctype: 'Customer' },
                format_result: function(result) {
                    // Split the default description into parts
                    const parts = (result.description || '').split('\n');
                    
                    // Reformat with better visual hierarchy
                    return `
                        <div style="line-height: 1.4;">
                            <strong style="display: block; margin-bottom: 2px;">
                                ${parts[0] || result.value}
                            </strong>
                            <small style="color: #666; font-size: 12px;">
                                ${parts[1] ? `<div>📍 ${parts[1]}</div>` : ''}
                                ${parts[2] ? `<div>🏢 ${parts[2]}</div>` : ''}
                            </small>
                        </div>
                    `;
                }
            };
        });
    }
});