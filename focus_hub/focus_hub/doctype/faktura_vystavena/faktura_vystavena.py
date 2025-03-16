import frappe
from frappe.model.document import Document

class FakturaVystavena(Document):
    def on_update(self):
        # 1. Check if a Prijmy record is already linked
        if self.linked_prijmy:
            return  # Avoid duplicate creation

        # 2. Create a new Prijmy document
        prijmy_doc = frappe.get_doc({
            "doctype": "Prijmy",
            "title": f"Invoice {self.invoice_number}",        # Or any title logic
            "external_id": self.name,              # Matches 'External ID' field
            "date_issued": self.date_issued,       # Matches 'date issued' field
            "customer_email": self.customer_email, # Matches 'customer email' field
            "total_value": self.total_with_tax or 0.0  # Matches 'total value' field
        })
        prijmy_doc.insert(ignore_permissions=True)

        # 3. Link the new Prijmy doc back to Faktura Vystavena
        self.linked_prijmy = prijmy_doc.name
        self.save(ignore_permissions=True)
