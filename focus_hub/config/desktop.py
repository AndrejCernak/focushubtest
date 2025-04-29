# File: apps/focus_hub/focus_hub/config/desktop.py
from frappe import _

def get_data():
    return [
        {
            "label": _("Faktúry"),
            "icon": "octicon octicon-file",
            "items": [
                {
                    "type": "doctype",
                    "name": "Faktura Vystavena",
                    "label": _("Faktúra Vystavená"),
                },
                {
                    "type": "doctype",
                    "name": "Faktura Prijata",
                    "label": _("Faktúra Prijatá"),
                }
            ]
        },
        {
            "label": _("Financie"),
            "icon": "octicon octicon-credit-card",
            "items": [
                {
                    "type": "doctype",
                    "name": "Prijmy",
                    "label": _("Príjmy"),
                },
                {
                    "type": "doctype",
                    "name": "Vydavky",
                    "label": _("Výdavky"),
                }
            ]
        },
        {
            "label": _("Ľudia"),
            "icon": "octicon octicon-person",
            "items": [
                {
                    "type": "doctype",
                    "name": "Customer",
                    "label": _("Zákazníci"),
                }
            ]
        }
    ]
