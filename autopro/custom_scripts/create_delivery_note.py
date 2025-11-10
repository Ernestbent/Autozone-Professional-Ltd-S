import frappe
from frappe import _

@frappe.whitelist()
def create_delivery_note_from_sales_order(source_name):
    """Create a Delivery Note from Sales Order"""
    try:
        # Import ERPNext helper
        from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note as erp_make_delivery_note

        # Generate the Delivery Note
        dn = erp_make_delivery_note(source_name)

        # Insert if new
        if dn.get("__islocal"):
            dn.insert(ignore_permissions=True)
            frappe.db.commit()

        # Return doc info for client-side routing
        return {"doctype": "Delivery Note", "name": dn.name}

    except Exception as e:
        frappe.throw(_("Could not create Delivery Note: {0}").format(str(e)))