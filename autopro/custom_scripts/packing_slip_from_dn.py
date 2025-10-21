import frappe

def populate_rate_amount(doc, method):
   
    if not doc.delivery_note:
        return

    # Fetch Delivery Note items
    dn_items = frappe.get_all(
        "Delivery Note Item",
        filters={"parent": doc.delivery_note},
        fields=["name", "item_code", "rate", "uom"],
    )

    dn_map = {d.item_code: d for d in dn_items}

    # Populate Packing Slip item fields
    for row in doc.items:
        if row.item_code in dn_map:
            dn = dn_map[row.item_code]
            row.custom_rate = dn.rate
            row.custom_amount = dn.rate * row.qty
            row.dn_detail = dn.name
            row.stock_uom = dn.uom
