import frappe
from frappe.model.document import Document

class FakturaVystavena(Document):
    def before_save(self):
        # Nastav variabilny_symbol na cislo_faktury, ak ešte nie je vyplnený
        if self.cislo_faktury and not self.variabilny_symbol:
            self.variabilny_symbol = self.cislo_faktury

    def on_update(self):
        # Preskoč ak už je prepojený záznam v Prijmy
        if self.linked_prijmy:
            return

        # Vytvor nový dokument Prijmy
        prijmy_doc = frappe.get_doc({
            "doctype": "Prijmy",
            "nazov": f"Faktúra {self.cislo_faktury}",
            "externe_id": self.name,
            "datum_vydania": self.datum_vydania,
            "email_zakaznika": self.email_zakaznika,
            "celkova_suma": self.celkom_s_danou or 0.0
        })
        prijmy_doc.insert(ignore_permissions=True)

        # Prepoj späť na túto faktúru
        self.linked_prijmy = prijmy_doc.name
        self.save(ignore_permissions=True)
