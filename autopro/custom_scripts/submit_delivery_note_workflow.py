import frappe

def restrict_next_state_if_dn_not_submitted(doc, method):
    if doc.workflow_state == "Delivery Note Created":
        dn_name = doc.get("delivery_note")
        if dn_name:
            dn_status = frappe.db.get_value("Delivery Note", dn_name, "docstatus")
            if dn_status != 1:
                frappe.throw("Cannot proceed: Delivery Note is not yet submitted.")
