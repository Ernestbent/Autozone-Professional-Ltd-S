# Copyright (c) 2025, Autozone Pro Ltd and contributors
# For license information, please see license.txt

# import frappe


import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        {"label": "Document Type", "fieldname": "document_type", "fieldtype": "Link", "options": "DocType", "width": 120},
        {"label": "Document ID", "fieldname": "document_id", "fieldtype": "Dynamic Link", "options": "document_type", "width": 150},
        {"label": "Document Title", "fieldname": "document_title", "fieldtype": "Data", "width": 200},
        {"label": "Date & Time", "fieldname": "date_time", "fieldtype": "Datetime", "width": 150},
        {"label": "User ID", "fieldname": "user_id", "fieldtype": "Link", "options": "User", "width": 120},
        {"label": "User Name", "fieldname": "user_name", "fieldtype": "Data", "width": 150},
        {"label": "Activity Type", "fieldname": "activity_type", "fieldtype": "Data", "width": 120},
        {"label": "Comment/Action", "fieldname": "comment_action", "fieldtype": "Text", "width": 300},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
        {"label": "ToDo Status", "fieldname": "todo_status", "fieldtype": "Data", "width": 100},
    ]


def get_data():
    query = """
        SELECT
            c.reference_doctype AS document_type,
            c.reference_name AS document_id,
            COALESCE(d.subject, c.reference_name) AS document_title,
            c.creation AS date_time,
            c.owner AS user_id,
            u.full_name AS user_name,
            c.comment_type AS activity_type,
            c.content AS comment_action,
            COALESCE(t.priority, 'Normal') AS priority,
            COALESCE(t.status, 'N/A') AS todo_status
        FROM `tabComment` c
        LEFT JOIN `tabUser` u ON u.name = c.owner
        LEFT JOIN `tabToDo` t ON t.reference_type = c.reference_doctype
                             AND t.reference_name = c.reference_name
        LEFT JOIN `tabCommunication` d ON d.reference_doctype = c.reference_doctype
                                      AND d.reference_name = c.reference_name
        WHERE c.comment_type IN ('Comment', 'Info', 'Assigned', 'Attachment')
        ORDER BY c.creation DESC
    """
    return frappe.db.sql(query, as_dict=True)
