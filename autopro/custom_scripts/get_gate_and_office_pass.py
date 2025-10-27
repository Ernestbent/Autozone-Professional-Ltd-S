import frappe

@frappe.whitelist()

def generate_gate_passes(delivery_note_name, office_gate_pass=None, store_gate_pass)
    dn = frappe.get_doc("Delivery Note", delivery_note_name)

    ##Generate if not provided
    if not office_gate_pass:
        office_gate_pass = frappe.model.naming.make_autoname("OGP-.YYYY,MM.-.####")

    if not store_gate_pass:
        store_gate_pass = frappe.model.naming.make_autoname("SGP-.YYYY,MM.-.####")

    dn.office_gate_pass = office_gate_pass
    dn.store_gate_pass = store_gate_pass
    dn.workflow_state = "In Transit"
    dn.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "office_gate_pass": office_gate_pass,
        "store_gate_pass": store_gate_pass
    }