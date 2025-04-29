import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class FakturaPrijata(Document):
    def before_save(self):
        # Nastav variabilny_symbol = cislo_faktury ak nie je vyplnený
        if self.cislo_faktury and not self.variabilny_symbol:
            self.variabilny_symbol = self.cislo_faktury

    def on_update(self):
        # 1. Skontroluj, či už je vytvorený záznam vo Vydavkoch
        if self.linked_vydavky:
            return  # Zamedz duplikácii

        # 2. Vytvor nový záznam Vydavky
        vydavky_doc = frappe.get_doc({
            "doctype": "Vydavky",
            "nazov": f"Faktúra {self.cislo_faktury}",
            "datum": self.datum_vydania or nowdate(),
            "suma": self.celkom_s_danou or 0.0
        })
        vydavky_doc.insert(ignore_permissions=True)

        # 3. Prepoj ho späť na Faktura Prijata
        self.linked_vydavky = vydavky_doc.name
        self.save(ignore_permissions=True)
