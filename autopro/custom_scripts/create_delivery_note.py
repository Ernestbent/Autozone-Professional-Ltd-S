import frappe
from frappe import _

@frappe.whitelist()
def create_delivery_note_from_sales_order(source_name):
    """Create Delivery Note and update Sales Order workflow state"""
    try:
        from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note as erp_make_delivery_note

        # Create Delivery Note
        delivery_note = erp_make_delivery_note(source_name)
        delivery_note.insert(ignore_permissions=True)
        frappe.db.commit()

        # Update Sales Order workflow state
        frappe.db.set_value("Sales Order", source_name, "workflow_state", "Delivery Note Created")

        # Return info for client-side routing
        return {"doctype": "Delivery Note", "name": delivery_note.name}

    except Exception as e:
        frappe.throw(_("Could not create Delivery Note: {0}").format(str(e)))
