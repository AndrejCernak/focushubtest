import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class FakturaPrijata(Document):
    def on_update(self):
        # If your doctype is submittable (has a Submit button).
        # Otherwise, use on_update or before_save.

        # 1. Check if we already created a Vydavky record
        if self.linked_vydavky:
            return  # Avoid creating duplicates

        # 2. Create a new Vydavky document
        vydavky_doc = frappe.get_doc({
            "doctype": "Vydavky",
            "title": f"Invoice {self.invoice_number}",  # or any other naming
            "date": self.date_issued or nowdate(),
            "amount": self.total_with_tax or 0.0,
            # Add more fields if needed (e.g. external_id, notes, etc.)
        })
        vydavky_doc.insert(ignore_permissions=True)

        # 3. Link it back to Faktura Prijata
        self.linked_vydavky = vydavky_doc.name
        self.save(ignore_permissions=True)
