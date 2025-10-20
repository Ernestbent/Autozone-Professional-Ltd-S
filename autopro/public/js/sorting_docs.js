frappe.listview_settings['*'] = {
    onload: function(listview) {
        // Override default sorting to descending by modified (most recent first)
        if (listview && listview.meta && listview.meta.sort_field && listview.meta.sort_order) {
            // Modify default sort field and order
            listview.page.sort_selector && listview.page.sort_selector.val(`${listview.meta.sort_field},desc`).change();
        } else {
            // Fallback: sort by modified date
            listview.page.sort_selector && listview.page.sort_selector.val('modified,desc').change();
        }
    }
};
