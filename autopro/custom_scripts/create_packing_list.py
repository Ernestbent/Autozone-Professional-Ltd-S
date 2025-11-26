import frappe
from frappe import _
from frappe.utils import today, get_time, now

@frappe.whitelist()
def create_packing_list_from_sales_order(source_name):
    try:
        # Get Sales Order (we only need it for validation and customer)
        so = frappe.get_doc("Sales Order", source_name)

        pl = frappe.new_doc("Packing List")

        # === AUTO-FILL SALES ORDER (both fields) ===
        pl.sales_order = source_name                    # Your original field
        pl.custom_sales_order = source_name             # Your custom field for Connections tab

        # === AUTO-FILL FROM DELIVERY NOTE (the source of truth) ===
        dn_name = frappe.db.sql("""
            SELECT parent 
            FROM `tabDelivery Note Item` 
            WHERE against_sales_order = %s 
              AND docstatus = 1 
            ORDER BY parent DESC 
            LIMIT 1
        """, source_name)

        if not dn_name or not dn_name[0][0]:
            frappe.throw(_("No submitted Delivery Note found for Sales Order {0}").format(source_name))

        dn_name = dn_name[0][0]
        dn_doc = frappe.get_doc("Delivery Note", dn_name)

        # Auto-fill everything from Delivery Note
        pl.delivery_note = dn_name
        pl.custom_customer = dn_doc.customer
        pl.customer = dn_doc.customer
        pl.customer_name = dn_doc.customer_name
        pl.company = dn_doc.company
        pl.custom_date = today()
        pl.custom_posting_time = str(get_time(now()))

        # === AUTO-FILL ITEMS FROM DELIVERY NOTE (actual shipped qty) ===
        for item in dn_doc.items:
            pl.append("table_ttya", {
                "item": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "uom": item.uom or item.stock_uom,
                "rate": item.rate or 0,
                "amount": item.amount or 0,
            })

        pl.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"doctype": "Packing List", "name": pl.name}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Packing List Failed")
        frappe.throw(_("Failed to create Packing List: {0}").format(str(e)))