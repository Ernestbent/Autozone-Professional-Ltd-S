import frappe

def execute(filters=None):
    columns = [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 120},
        {"label": "Item Description", "fieldname": "item_description", "fieldtype": "Data", "width": 200},
        {"label": "Sales Order Date", "fieldname": "sales_order_date", "fieldtype": "Date", "width": 120},
        {"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 120},
        {"label": "Delivery Date", "fieldname": "delivery_date", "fieldtype": "Date", "width": 120},
        {"label": "Invoice Number", "fieldname": "invoice_number", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
        {"label": "Customer ID", "fieldname": "customer_id", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Sales Order Number", "fieldname": "sales_order_number", "fieldtype": "Link", "options": "Sales Order", "width": 150},
        {"label": "Delivery Note Number", "fieldname": "delivery_note_number", "fieldtype": "Link", "options": "Delivery Note", "width": 150},
        {"label": "Billed Quantity", "fieldname": "billed_quantity", "fieldtype": "Float", "width": 100},
        {"label": "Standard Selling Price", "fieldname": "standard_selling_price", "fieldtype": "Currency", "width": 120},
        {"label": "Rate Amount", "fieldname": "rate_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Total Amount With Discount", "fieldname": "total_amount_with_discount", "fieldtype": "Currency", "width": 150},
        {"label": "Total Amount Without Discount", "fieldname": "total_amount_without_discount", "fieldtype": "Currency", "width": 150},
        {"label": "Discount Percentage", "fieldname": "discount_percentage", "fieldtype": "Percent", "width": 120},
        {"label": "Sales Person", "fieldname": "sales_person", "fieldtype": "Data", "width": 200},
        {"label": "District", "fieldname": "district", "fieldtype": "Data", "width": 120},
        {"label": "Region", "fieldname": "region", "fieldtype": "Data", "width": 120},
        {"label": "Route", "fieldname": "route", "fieldtype": "Data", "width": 120},
        {"label": "Grand Total After Discount", "fieldname": "grand_total_after_discount", "fieldtype": "Currency", "width": 150},
        {"label": "Grand Total Before Discount", "fieldname": "grand_total_before_discount", "fieldtype": "Currency", "width": 150},
    ]

    data = frappe.db.sql("""
        SELECT
            sii.item_code AS item_code,
            sii.item_name AS item_description,
            so.transaction_date AS sales_order_date,
            si.posting_date AS invoice_date,
            dn.posting_date AS delivery_date,
            si.name AS invoice_number,
            si.customer AS customer_id,
            so.name AS sales_order_number,
            dn.name AS delivery_note_number,
            sii.qty AS billed_quantity,
            i.standard_rate AS standard_selling_price,
            sii.rate AS rate_amount,
            sii.amount AS total_amount_with_discount,
            (sii.qty * sii.rate / (1 - IFNULL(sii.discount_percentage, 0) / 100)) AS total_amount_without_discount,
            sii.discount_percentage AS discount_percentage,
            GROUP_CONCAT(st.sales_person) AS sales_person,
            LOWER(COALESCE(c.district, '')) AS district,
            LOWER(COALESCE(c.region, '')) AS region,
            LOWER(COALESCE(c.route, '')) AS route,
            si.grand_total AS grand_total_after_discount,
            (SELECT SUM(sii_inner.qty * sii_inner.rate / (1 - IFNULL(sii_inner.discount_percentage, 0) / 100)) 
             FROM `tabSales Invoice Item` sii_inner 
             WHERE sii_inner.parent = si.name) + IFNULL(si.discount_amount, 0) AS grand_total_before_discount
        FROM `tabSales Invoice` si
        INNER JOIN `tabSales Invoice Item` sii ON si.name = sii.parent
        LEFT JOIN `tabSales Order` so ON sii.sales_order = so.name
        LEFT JOIN `tabDelivery Note` dn ON sii.delivery_note = dn.name
        LEFT JOIN `tabItem` i ON sii.item_code = i.name
        LEFT JOIN `tabSales Team` st ON si.name = st.parent
        LEFT JOIN `tabCustomer` c ON si.customer = c.name
        WHERE si.docstatus = 1
        GROUP BY sii.name, si.name, so.name, dn.name, c.name
        ORDER BY si.posting_date DESC, si.name, sii.item_code
    """, as_dict=True)

    return columns, data
