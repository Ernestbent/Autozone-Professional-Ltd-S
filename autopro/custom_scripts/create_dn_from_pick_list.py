# import frappe
# from erpnext.stock.doctype.pick_list.pick_list import make_delivery_note as erp_make_delivery_note

# @frappe.whitelist()
# def create_delivery_note_from_pick_list(pick_list_name):
#     """
#     Creates a Draft Delivery Note from a Pick List
#     and updates linked Sales Order workflow state
#     """
#     # Create Delivery Note from Pick List
#     delivery_note = erp_make_delivery_note(pick_list_name)
#     delivery_note.insert(ignore_permissions=True)  # stays Draft

#     # Update linked Sales Orders workflow
#     for item in delivery_note.items:
#         so_name = item.against_sales_order
#         if so_name:
#             frappe.db.set_value("Sales Order", so_name, "workflow_state", "Delivery Note Created")

#     frappe.db.commit()
#     return {"doctype": delivery_note.doctype, "name": delivery_note.name}
