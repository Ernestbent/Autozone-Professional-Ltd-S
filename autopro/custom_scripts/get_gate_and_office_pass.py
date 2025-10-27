import frappe
from frappe import _

@frappe.whitelist()
def generate_gate_pass():
    """
    Generate office and store gate pass numbers without requiring a saved Delivery Note
    """
    try:
        # Define the naming series
        office_series = "OGP-.YYYY.-"  # Office Gate Pass
        store_series = "SGP-.YYYY.-"   # Store Gate Pass

        # Generate autonames
        office_gate_pass = frappe.model.naming.make_autoname(office_series)
        store_gate_pass = frappe.model.naming.make_autoname(store_series)

        return {
            "custom_office_gate_pass": office_gate_pass,
            "custom_store_gate_pass": store_gate_pass
        }
    except Exception as e:
        frappe.log_error(f"Error generating gate passes: {str(e)}")
        frappe.throw(_("Failed to generate gate passes: {0}").format(str(e)))