import frappe

def on_submit(doc, method=None):
    """
    Called when Delivery Note is submitted.
    Updates ALL linked Sales Orders' workflow_state to "Delivery Note Created"
    """
    TARGET_STATE = "Delivery Note Created"

    # Collect unique Sales Orders from DN items
    so_names = set()

    for item in doc.items:
        # 1. Direct link (Create DN from SO)
        if item.against_sales_order:
            so_names.add(item.against_sales_order)

        # 2. Via Pick List (Create DN from Pick List)
        elif doc.pick_list:
            pl_so = get_so_from_pick_list(doc.pick_list, item.item_code, item.warehouse)
            if pl_so:
                so_names.add(pl_so)

    # Update each Sales Order
    for so_name in so_names:
        try:
            so = frappe.get_doc("Sales Order", so_name)

            if so.workflow_state == TARGET_STATE:
                continue  # Already updated

            so.workflow_state = TARGET_STATE
            so.save(ignore_permissions=True)
            frappe.db.commit()

            frappe.msgprint(
                f"Sales Order <b>{so_name}</b> → <b>{TARGET_STATE}</b>",
                indicator="green",
                alert=True
            )

        except Exception as e:
            frappe.log_error(
                message=frappe.get_traceback(),
                title=f"Failed to update SO {so_name} on DN {doc.name}"
            )