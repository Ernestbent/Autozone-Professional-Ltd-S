frappe.listview_settings['Item Price'] = {
    add_columns: [
        {
            fieldname: 'custom_availablel_qty',
            label: __('Available Qty'),
            width: 120
        }
    ],
    onload: function(listview) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Item Price",
                fields: ["name", "item_code"],
                limit_page_length: 1000
            },
            callback: function(response) {
                const itemCodes = [...new Set(response.message.map(row => row.item_code))];

                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Bin",
                        filters: {
                            item_code: ["in", itemCodes]
                        },
                        fields: ["item_code", "actual_qty"],
                        limit_page_length: 1000
                    },
                    callback: function(res) {
                        const stock_map = {};
                        res.message.forEach(bin => {
                            stock_map[bin.item_code] = (stock_map[bin.item_code] || 0) + bin.actual_qty;
                        });

                        listview.data.forEach(row => {
                            row.custom_availablel_qty = stock_map[row.item_code] || 0;
                        });

                        listview.refresh();
                    }
                });
            }
        });
    }
};
