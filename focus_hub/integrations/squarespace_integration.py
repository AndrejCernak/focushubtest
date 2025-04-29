import requests
import frappe
from frappe.utils import now_datetime

def fetch_and_write_orders():
    url = "https://api.squarespace.com/1.0/commerce/orders"
    payload = {}
    headers = {
        "Authorization": "Bearer 1ea8f560-c83b-48c4-a077-f79c5911d927",
        "Content-Type": "application/json",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)

    try:
        data = response.json()
    except Exception as e:
        frappe.log_error(message=str(e), title="Squarespace JSON Parse Error")
        return "Chyba pri spracovaní JSON odpovede"

    orders = data.get("result", [])
    print(f"Načítaných {len(orders)} objednávok zo 'result'")

    for order in orders:
        process_order(order)

    return f"Spracovaných {len(orders)} objednávok."


def process_order(order):
    externe_id = order.get("id")
    cislo_objednavky = order.get("orderNumber")
    vytvorene_raw = order.get("createdOn")
    email_zakaznika = order.get("customerEmail")

    cena_spolu_raw = order.get("grandTotal", {}).get("value", "0.00")
    try:
        celkova_suma = float(cena_spolu_raw)
    except ValueError:
        celkova_suma = 0.0

    if frappe.db.exists("Prijmy", {"externe_id": externe_id}):
        return

    try:
        datum_vydania = vytvorene_raw.split("T")[0] if vytvorene_raw else None

        doc = frappe.get_doc({
            "doctype": "Prijmy",
            "externe_id": externe_id,
            "nazov": f"Objednávka {cislo_objednavky}",
            "datum_vydania": datum_vydania,
            "email_zakaznika": email_zakaznika,
            "celkova_suma": celkova_suma
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"Záznam Príjmy vytvorený pre objednávku {cislo_objednavky}")
    except Exception as e:
        frappe.log_error(message=str(e), title="Chyba pri vytváraní záznamu Prijmy")


def main():
    return fetch_and_write_orders()
