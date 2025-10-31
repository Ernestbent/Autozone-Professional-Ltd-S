import frappe
from frappe import _

def check_packing_slip(doc, method):
    # Correctly use a string for the dictionary key
    ps_count = frappe.db.count("Packing Slip", {"delivery_note": doc.name})
    
    if ps_count == 0:
        frappe.throw(_("Cannot submit Delivery Note {0} because no Packing Slip exists.").format(doc.name))
