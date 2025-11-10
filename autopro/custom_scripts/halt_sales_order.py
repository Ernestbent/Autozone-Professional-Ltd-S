# import frappe

# def check_courier_details(doc, method):
#     """
#     Server-side workflow hook to halt approval if no Courier Details exist.
#     """
#     if doc.workflow_state == "Approved":
#         # Check if any Courier Details are linked via custom_sales_order
#         linked = frappe.get_all(
#             "Courier Details",
#             filters={"custom_sales_order": doc.name},
#             limit_page_length=1
#         )
#         if not linked:
#             frappe.throw(
#                 f"Cannot proceed: No Courier Details found for Sales Order {doc.name}."
#             )
