import frappe

@frappe.whitelist()
def has_courier_details(sales_order_name):
    """Returns True if at least one Courier Details record exists for this Sales Order."""
    return frappe.db.exists("Courier Details", {"custom_sales_order": sales_order_name}) is not None
