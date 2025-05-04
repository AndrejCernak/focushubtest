import frappe

def load_workspaces():
    json_files = [
        "faktury_workspace.json",
        "vystavene_faktury_workspace.json",
        "prijate_faktury_workspace.json",
        "vydavky_workspace.json",
        "clenovia_workspace.json"
    ]

    for file in json_files:
        frappe.reload_doc("focus_hub", "workspace", file.replace(".json", ""))
