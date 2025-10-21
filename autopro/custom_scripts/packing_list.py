import frappe

@frappe.whitelist()
def fetch_delivery_note_items(delivery_note):
    """
    Fetch items from Delivery Note and return as a list of dicts
    to populate Packing Slip Item child table with custom rate and custom amount.
    """
    if not delivery_note:
        frappe.throw("Delivery Note is required")

    items = frappe.get_all(
        "Delivery Note Item",
        filters={"parent": delivery_note},  
        fields=[
            "name as dn_detail",
            "item_code",
            "item_name",
            "qty",
            "uom",
            "rate",
            "amount"
        ],
        order_by="idx"
    )

    if not items:
        frappe.throw(f"No items found for Delivery Note {delivery_note}")

    return [{
        "dn_detail": i.dn_detail,       
        "item_code": i.item_code,
        "item_name": i.item_name,
        "qty": i.qty,
        "stock_uom": i.uom,
        "custom_rate": i.rate,
        "custom_amount": i.rate * i.qty
    } for i in items]
