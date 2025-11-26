# import frappe
# from frappe import _

# @frappe.whitelist()
# def create_pick_list_from_sales_order(source_name):
#     """Create a Pick List from Sales Order only if not exists"""
#     try:
#         # Check if Pick List already exists
#         existing = frappe.get_list("Pick List", filters={"sales_order": source_name}, limit_page_length=1)
#         if existing:
#             return {"doctype": "Pick List", "name": existing[0].name}

#         # Create Pick List if not found
#         from erpnext.selling.doctype.sales_order.sales_order import create_pick_list as erp_create_pick_list
#         pick_list = erp_create_pick_list(source_name)

#         if pick_list.docstatus == 0:
#             pick_list.save(ignore_permissions=True)
#             frappe.db.commit()

#         return {"doctype": "Pick List", "name": pick_list.name}

#     except Exception as e:
#         frappe.throw(_("Could not create Pick List: {0}").format(str(e)))
