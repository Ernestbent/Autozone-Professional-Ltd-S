# import frappe
# from erpnext.stock.doctype.pick_list.pick_list import make_delivery_note as erp_make_delivery_note

# @frappe.whitelist()
# def create_delivery_note_from_pick_list(pick_list_name):
#     """
#     Creates a Draft Delivery Note from a Pick List
#     and updates linked Sales Order workflow state only if it hasn't yet moved past 'Create Delivery Note'.
#     """
#     # Create Delivery Note from Pick List
#     delivery_note = erp_make_delivery_note(pick_list_name)
#     delivery_note.insert(ignore_permissions=True)  # stays Draft

#     # Workflow states
#     FINAL_STATES = ["Completed", "Cancelled"]
#     TARGET_STATE = "Delivery Note Created"
#     PREVIOUS_STATE = "Create Delivery Note"

#     # Update linked Sales Orders workflow
#     for item in delivery_note.items:
#         so_name = item.against_sales_order
#         if not so_name:
#             continue

#         current_state = frappe.db.get_value("Sales Order", so_name, "workflow_state")

#         # Only update if currently in 'Create Delivery Note'
#         if current_state == PREVIOUS_STATE:
#             frappe.db.set_value("Sales Order", so_name, "workflow_state", TARGET_STATE)

#     frappe.db.commit()
#     return {"doctype": delivery_note.doctype, "name": delivery_note.name}
