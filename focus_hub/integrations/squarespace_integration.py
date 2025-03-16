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
        return "Error parsing JSON"

    orders = data.get("result", [])
    print(f"Fetched {len(orders)} orders from 'result'")

    for order in orders:
        process_order(order)

    return f"Processed {len(orders)} orders."

def process_order(order):
    """
    Extracts basic info from the Squarespace order and inserts a new record into the Prijmy doctype.
    Adjust field names as needed for your actual doctype fields.
    """
    external_id = order.get("id")
    order_number = order.get("orderNumber")
    created_on = order.get("createdOn")  
    customer_email = order.get("customerEmail")

    grand_total_str = order.get("grandTotal", {}).get("value", "0.00")
    try:
        total_value = float(grand_total_str)
    except ValueError:
        total_value = 0.0

    if frappe.db.exists("Prijmy", {"external_id": external_id}):
        return

    try:
        date_issued = created_on.split("T")[0] if created_on else None

        doc = frappe.get_doc({
            "doctype": "Prijmy",
            "external_id": external_id,
            "order_number": order_number,
            "date_issued": date_issued,
            "customer_email": customer_email,
            "total_value": total_value,
            "last_synced": now_datetime(),
            "title": f"Order {order_number}"
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"Created Prijmy record for order {order_number}")
    except Exception as e:
        frappe.log_error(message=str(e), title="Error Creating Prijmy Record")

def main():
    return fetch_and_write_orders()
