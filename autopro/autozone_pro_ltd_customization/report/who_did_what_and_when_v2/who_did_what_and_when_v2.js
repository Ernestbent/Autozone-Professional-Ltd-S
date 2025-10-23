// Copyright (c) 2025, Autozone Pro Ltd and contributors
// For license information, please see license.txt

frappe.query_reports["Who Did What and When v2"] = {
	"filters": [
		{
      "fieldname": "from_date",
      "label": "From Date",
      "fieldtype": "Date"
    },
    {
      "fieldname": "to_date",
      "label": "To Date",
      "fieldtype": "Date"
    },
    {
      "fieldname": "user",
      "label": "User",
      "fieldtype": "Link",
      "options": "User"
    }

	]
};
