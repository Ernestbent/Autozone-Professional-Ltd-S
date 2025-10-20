import frappe
import json

def get_user(docname, from_state, to_state):
    logs = frappe.get_all(
        "Version",
        filters={"ref_doctype": "Sales Order", "docname": docname},
        fields=["owner", "data"],
        order_by="creation asc"
    )
    for v in logs:
        if v.data:
            try:
                changes = json.loads(v.data).get("changed", [])
                for change in changes:
                    if change[0] == "workflow_state" and change[1] == from_state and change[2] == to_state:
                        return frappe.db.get_value("User", v.owner, "full_name")
            except Exception:
                pass
    return None

if not doc.sales_person:
    doc.sales_person = get_user(doc.name, "Draft", "Pending Credit Approval")
if not doc.approved_by:
    doc.approved_by = get_user(doc.name, "Pending Credit Approval", "Approved")
if not doc.billed_by:
    doc.billed_by = get_user(doc.name, "Approved", "Being Delivered")