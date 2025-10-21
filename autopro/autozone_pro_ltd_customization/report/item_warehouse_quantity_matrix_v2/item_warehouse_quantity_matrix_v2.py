import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Data", "width": 150},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 250},
        {"label": "Catherine Stock - APL", "fieldname": "catherine_stock_apl", "fieldtype": "Float", "width": 120},
        {"label": "Damages - APL", "fieldname": "damages_apl", "fieldtype": "Float", "width": 120},
        {"label": "Davis Stock - APL", "fieldname": "davis_stock_apl", "fieldtype": "Float", "width": 120},
        {"label": "Gagan Stock - APL", "fieldname": "gagan_stock_apl", "fieldtype": "Float", "width": 120},
        {"label": "Ishaq Stock - APL", "fieldname": "ishaq_stock_apl", "fieldtype": "Float", "width": 120},
        {"label": "Main Loc - APL", "fieldname": "main_loc_apl", "fieldtype": "Float", "width": 120},
        {"label": "Office Semple Stock - APL", "fieldname": "office_semple_stock_apl", "fieldtype": "Float", "width": 140},
        {"label": "Saif Stock - APL", "fieldname": "saif_stock_apl", "fieldtype": "Float", "width": 120},
        {"label": "Total Qty", "fieldname": "total_qty", "fieldtype": "Float", "width": 120},
    ]


def get_data(filters=None):
    query = """
        WITH item_quantities AS (
            SELECT 
                i.item_code,
                i.item_name,
                SUM(CASE WHEN b.warehouse = 'Catherine Stock - APL' THEN b.actual_qty ELSE 0 END) as catherine_stock_apl,
                SUM(CASE WHEN b.warehouse = 'Damages - APL' THEN b.actual_qty ELSE 0 END) as damages_apl,
                SUM(CASE WHEN b.warehouse = 'Davis Stock - APL' THEN b.actual_qty ELSE 0 END) as davis_stock_apl, 
                SUM(CASE WHEN b.warehouse = 'Gagan Stock - APL' THEN b.actual_qty ELSE 0 END) as gagan_stock_apl, 
                SUM(CASE WHEN b.warehouse = 'Ishaq Stock - APL' THEN b.actual_qty ELSE 0 END) as ishaq_stock_apl,
                SUM(CASE WHEN b.warehouse = 'Main Loc - APL' THEN b.actual_qty ELSE 0 END) as main_loc_apl, 
                SUM(CASE WHEN b.warehouse = 'Office Semple Stock - APL' THEN b.actual_qty ELSE 0 END) as office_semple_stock_apl,
                SUM(CASE WHEN b.warehouse = 'Saif Stock - APL' THEN b.actual_qty ELSE 0 END) as saif_stock_apl, 
                SUM(b.actual_qty) as total_qty
            FROM `tabItem` i
            LEFT JOIN `tabBin` b ON i.item_code = b.item_code
            WHERE i.disabled = 0
            GROUP BY i.item_code, i.item_name
        )
        SELECT 
            item_code,
            item_name,
            catherine_stock_apl,
            damages_apl,
            davis_stock_apl, 
            gagan_stock_apl, 
            ishaq_stock_apl,
            main_loc_apl, 
            office_semple_stock_apl,
            saif_stock_apl, 
            total_qty
        FROM item_quantities
        ORDER BY item_code
    """
    return frappe.db.sql(query, as_dict=True)
