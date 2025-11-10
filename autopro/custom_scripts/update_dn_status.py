import frappe

def on_submit(doc, method=None):
    """
    Called when Delivery Note is submitted.
    Updates all linked Sales Orders that have NOT yet reached
    'Delivery Note Created' workflow state.
    """
    TARGET_STATE = "Delivery Note Created"
    FINAL_STATES = ["Completed", "Cancelled"]  # states we don't touch

    # Collect unique Sales Orders from DN items
    so_names = set()

    for item in doc.items:
        # 1. Direct link (DN from SO)
        if item.against_sales_order:
            so_names.add(item.against_sales_order)

        # 2. Via Pick List (DN from Pick List)
        elif doc.pick_list:
            pl_so = get_so_from_pick_list(doc.pick_list, item.item_code, item.warehouse)
            if pl_so:
                so_names.add(pl_so)

    # Update each Sales Order safely
    for so_name in so_names:
        try:
            so = frappe.get_doc("Sales Order", so_name)

            # Skip SOs that already reached target or are in final states
            if so.workflow_state == TARGET_STATE or so.workflow_state in FINAL_STATES:
                continue

            # Update workflow state
            so.workflow_state = TARGET_STATE
            so.save(ignore_permissions=True)
            frappe.db.commit()

            # Optional: show alert for each updated SO
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
