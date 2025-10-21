import frappe
from frappe.query_builder import DocType, functions as fn

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Sales Order Date", "fieldname": "sales_order_date", "fieldtype": "Date", "width": 150},
        {"label": "Delivery Date", "fieldname": "delivery_date", "fieldtype": "Date", "width": 150},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Actual Item Price", "fieldname": "actual_item_price", "fieldtype": "Currency", "width": 150},
        {"label": "Total Amount Without Discount", "fieldname": "total_amount_without_discount", "fieldtype": "Currency", "width": 200},
        {"label": "Item Discount Percentage", "fieldname": "item_discount_percentage", "fieldtype": "Percent", "width": 180},
        {"label": "Item Discount Amount", "fieldname": "item_discount_amount", "fieldtype": "Currency", "width": 180},
        {"label": "Order Discount Amount", "fieldname": "order_discount_amount", "fieldtype": "Currency", "width": 180},
        {"label": "Sales Person", "fieldname": "sales_person", "fieldtype": "Data", "width": 150},
    ]


def get_data(filters=None):
    SO = DocType("Sales Order")
    SOI = DocType("Sales Order Item")
    ST = DocType("Sales Team")

    query = (
        frappe.qb.from_(SO)
        .left_join(SOI)
        .on(SOI.parent == SO.name)
        .left_join(ST)
        .on(ST.parent == SO.name)
        .select(
            SO.transaction_date.as_("sales_order_date"),
            SOI.delivery_date.as_("delivery_date"),
            SOI.item_name.as_("item_name"),
            SOI.rate.as_("actual_item_price"),
            (SOI.qty * SOI.price_list_rate).as_("total_amount_without_discount"),
            fn.Coalesce(SOI.discount_percentage, 0).as_("item_discount_percentage"),
            fn.Coalesce(SOI.discount_amount, 0).as_("item_discount_amount"),
            fn.Coalesce(SO.discount_amount, 0).as_("order_discount_amount"),
            ST.sales_person.as_("sales_person"),
        )
        .where(SO.docstatus == 1)
        .orderby(SO.transaction_date, order=frappe.qb.desc)
        .orderby(SO.name)
        .orderby(SOI.item_name)
    )

    return query.run(as_dict=True)
