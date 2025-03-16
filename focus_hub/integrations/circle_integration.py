import requests
import frappe
from frappe.utils import now_datetime
from datetime import datetime

def fetch_and_write_circle_customers():
    
    circle_host = "https://focus-club.atum.sk/api/admin/v2"
    circle_api_key = "GK8JG2tXiND4619QYVmwt23pUGZHtp6o"  

    url = f"{circle_host}/community_members"
    
    headers = {
        "Authorization": f"Bearer {circle_api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        frappe.log_error(title="Circle API Error", message=str(e))
        return f"Error fetching customers: {e}"
    
    data = response.json()
    records = data.get("records", [])
    frappe.msgprint(f"Fetched {len(records)} customers from Circle")
    
    for record in records:
        process_circle_customer(record)
    
    return f"Processed {len(records)} customers."


def process_circle_customer(record):
    external_id = record.get("id")
    full_name = record.get("name") or f"{record.get('first_name', '')} {record.get('last_name', '')}".strip()
    email = record.get("email")
    raw_created = record.get("created_at") 

    created_dt = None
    if raw_created:
        try:
            created_dt = datetime.strptime(raw_created, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            created_dt = datetime.strptime(raw_created, "%Y-%m-%dT%H:%M:%SZ")

    tags = record.get("member_tags", []) 
    if tags:
        tag_string = ", ".join(tag["name"] for tag in tags if tag.get("name"))
    else:
        tag_string = ""

    if frappe.db.exists("Customer", {"external_id": external_id}):
        return

    try:
        doc = frappe.get_doc({
            "doctype": "Customer",
            "external_id": external_id,
            "customer_name": full_name,
            "email": email,
            "created_at": created_dt,   
            "member_tag": tag_string,
            "last_synced": now_datetime(),
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(f"Created Customer record for {full_name}")
    except Exception as e:
        frappe.log_error(title="Error Creating Customer", message=str(e))


def main():
    """
    Entry point for testing via bench execute:
      bench --site your_site_name execute your_app.integrations.circle_customers.main
    """
    return fetch_and_write_circle_customers()
