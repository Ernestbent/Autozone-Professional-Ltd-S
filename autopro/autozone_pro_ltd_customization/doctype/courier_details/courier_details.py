# Copyright (c) 2025, Autozone Pro Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CourierDetails(Document):
	def validate(self):
		self.full_name = self.get_full_name()

	
	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"

	