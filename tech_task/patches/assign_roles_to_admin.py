import frappe

def execute():
    roles = ["Maintenance Team", "Maintenance Team Supervisor"]
    user = frappe.get_doc("User", "Administrator")

    for role_name in roles:
        if not frappe.db.exists("Has Role", {"parent": "Administrator", "role": role_name}):
            user.append("roles", {"role": role_name})
    
    user.save(ignore_permissions=True)
    frappe.db.commit()
