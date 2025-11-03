# import frappe
# from frappe import _

# def validate_packing_slip(doc, method):
#     if not doc.delivery_note:
#         frappe.throw(_("Delivery Note is required for Packing Slip."))

#     # Calculate total quantity from items
#     total_qty = sum(item.qty or 0 for item in doc.items)

#     # Calculate totals from custom_box_details
#     total_weight = 0.0
#     total_expense = 0.0
#     total_box_qty = 0.0

#     for box in doc.custom_box_details:
#         if not box.box_identifier:
#             frappe.throw(_("Box Identifier is mandatory for row {0}").format(box.idx))
#         total_weight += box.weight_of_box or 0.0
#         total_expense += box.expense_of_box or 0.0
#         total_box_qty += box.quantity or 0.0

#     # Validate box quantities against Delivery Note
#     dn = frappe.get_doc('Delivery Note', doc.delivery_note)
#     dn_total_qty = dn.total_qty or 0
#     if total_box_qty > dn_total_qty:
#         frappe.throw(_("Total quantity in boxes ({0}) exceeds Delivery Note total quantity ({1}).").format(total_box_qty, dn_total_qty))
#     if total_box_qty != total_qty:
#         frappe.throw(_("Total quantity in boxes ({0}) does not match total quantity in items ({1}).").format(total_box_qty, total_qty))

#     # Set totals
#     doc.custom_total_qty = total_qty
#     doc.custom_total_boxes = len(doc.custom_box_details)
#     doc.custom_total_box_weight = total_weight
#     doc.custom_billed_amount = total_expense

#     # Update Delivery Note with expenses (if custom field exists)
#     if doc.delivery_note and hasattr(dn, 'total_additional_costs'):
#         dn.total_additional_costs = (dn.total_additional_costs or 0) + total_expense
#         dn.save()