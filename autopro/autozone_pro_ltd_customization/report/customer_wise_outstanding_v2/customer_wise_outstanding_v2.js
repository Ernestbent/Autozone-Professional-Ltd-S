frappe.query_reports["Customer-wise Outstanding"] = {
    formatter: function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // Color formatting for Debit, Credit, Balance
        if (["debit", "credit", "balance"].includes(column.fieldname)) {
            const num = parseFloat(value?.replace(/,/g, '')) || 0;
            if (column.fieldname === "balance") {
                if (num > 0.01) value = `<span style="color:#d9534f;font-weight:bold;">${value}</span>`;
                else if (num < -0.01) value = `<span style="color:#5bc0de;font-weight:bold;">${value}</span>`;
                else value = `<span style="color:#5cb85c;">${value}</span>`;
            }
        }

        // Status coloring
        if (column.fieldname === "status") {
            if (data.status === "Outstanding")
                value = `<span style="color:#d9534f;font-weight:bold;">${value}</span>`;
            else if (data.status === "Advance")
                value = `<span style="color:#5bc0de;font-weight:bold;">${value}</span>`;
            else
                value = `<span style="color:#5cb85c;font-weight:bold;">${value}</span>`;
        }

        // Tooltip for ageing
        if (column.fieldname === "ageing_days") {
            value = `<span title="Days since voucher date">${value}</span>`;
        }

        return value;
    },

    onload_post_render: function (report) {
        let rows = report.data || [];
        let grouped = {};

        rows.forEach(d => {
            const cust = d.customer_name || d.account;
            if (!grouped[cust]) grouped[cust] = [];
            grouped[cust].push(d);
        });

        let new_data = [];
        Object.keys(grouped).forEach(cust => {
            let total_debit = 0, total_credit = 0, total_balance = 0;
            grouped[cust].forEach(d => {
                total_debit += d.debit || 0;
                total_credit += d.credit || 0;
                total_balance += d.balance || 0;
                new_data.push(d);
            });

            new_data.push({
                customer_name: cust + " (Subtotal)",
                debit: total_debit,
                credit: total_credit,
                balance: total_balance,
                status: total_balance > 0.01 ? "Outstanding" :
                        total_balance < -0.01 ? "Advance" : "Settled",
                voucher_number: "",
                voucher_date: "",
                ageing_days: "",
                sales_person: ""
            });
        });

        report.data = new_data;
        report.refresh();
    }
};
