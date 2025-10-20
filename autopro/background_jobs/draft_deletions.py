import frappe

def execute():
    # Use frappe object directly (available in scheduler context)
    cutoff_date = frappe.utils.add_days(frappe.utils.getdate(), -3)  # 3 days ago, e.g., August 31, 2025
    frappe.msgprint(f"Deleting drafts older than: {cutoff_date}")

    # Fetch all draft Sales Orders older than 3 days
    draft_orders = frappe.get_all("Sales Order", 
                                 filters={
                                     "docstatus": 0,  # Draft
                                     "modified": ["<", cutoff_date]
                                 },
                                 fields=["name", "owner", "modified"])

    if not draft_orders:
        frappe.msgprint("No draft Sales Orders older than 3 days found.")
        return

    deleted_count = 0
    for order in draft_orders:
        try:
            # Delete the Sales Order
            frappe.delete_doc("Sales Order", order.name)
            deleted_count += 1
            frappe.msgprint(f"Deleted draft Sales Order: {order.name} (Owner: {order.owner}, Modified: {order.modified})")
        except Exception as e:
            frappe.log_error(f"Failed to delete {order.name}: {str(e)}")

    frappe.msgprint(f"Total draft Sales Orders deleted: {deleted_count}")