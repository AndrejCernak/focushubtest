import requests
import frappe
from frappe.utils import now_datetime
from datetime import datetime

def fetch_and_write_circle_customers():
    """
    Fetch members from the Circle API and insert them as 'Clenovia' documents in Frappe.
    """
    circle_host = "https://focus-club.atum.sk/api/admin/v2"
    circle_api_key = "GK8JG2tXiND4619QYVmwt23pUGZHtp6o"

    headers = {
        "Authorization": f"Bearer {circle_api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    page = 1
    total_processed = 0

    try:
        while True:
            url = f"{circle_host}/community_members?page={page}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            records = data.get("records", [])

            frappe.msgprint(f"Strana {page}: načítaných {len(records)} členov z Circle")

            for record in records:
                process_circle_clen(record)
                total_processed += 1

            if not data.get("has_next_page"):
                break

            page += 1

    except Exception as e:
        frappe.log_error(title="Circle API Error", message=str(e))
        return f"Chyba pri načítaní členov: {e}"

    return f"Spracovaných {total_processed} členov zo všetkých strán."


def process_circle_clen(record):
    """
    Create a new 'Clenovia' document from a Circle API record if it doesn't already exist.
    """
    externe_id = record.get("id")
    meno_clena = record.get("name") or f"{record.get('first_name', '')} {record.get('last_name', '')}".strip()
    email = record.get("email")
    raw_created = record.get("created_at")

    vytvorene = None
    if raw_created:
        try:
            vytvorene = datetime.strptime(raw_created, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            vytvorene = datetime.strptime(raw_created, "%Y-%m-%dT%H:%M:%SZ")

    tagy = record.get("member_tags", [])
    clenstvo = ", ".join(tag["name"] for tag in tagy if tag.get("name")) if tagy else ""

    if frappe.db.exists("Clenovia", {"externe_id": externe_id}):
        return

    try:
        doc = frappe.get_doc({
            "doctype": "Clenovia",
            "externe_id": externe_id,
            "meno_zakaznika": meno_clena,
            "email": email,
            "vytvorene": vytvorene,
            "clenstvo": clenstvo,
            "naposledy_synchronizovane": now_datetime(),
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(f"Záznam člena vytvorený pre: {meno_clena}")
    except Exception as e:
        frappe.log_error(title="Chyba pri vytváraní člena", message=str(e))


def main():
    """
    Spustenie na testovanie cez bench execute:
      bench --site focushub.localhost execute focus_hub.integrations.circle_integration.main
    """
    return fetch_and_write_circle_customers()


