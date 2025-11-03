import frappe
from frappe import _

@frappe.whitelist()
def create_pick_list_from_sales_order(source_name):
    """Create a Pick List from Sales Order and prefill all items"""
    try:
        # Import the ERPNext helper
        from erpnext.selling.doctype.sales_order.sales_order import create_pick_list as erp_create_pick_list

        # Generate the Pick List from the Sales Order
        pick_list = erp_create_pick_list(source_name)

        # Check if doc is already inserted
        if not pick_list.get("__islocal"):  # already inserted
            pass
        else:
            pick_list.insert(ignore_permissions=True)
            frappe.db.commit()

        # Return doc info for client-side routing
        return {"doctype": "Pick List", "name": pick_list.name}

    except Exception as e:
        frappe.throw(_("Could not create Pick List: {0}").format(str(e)))
