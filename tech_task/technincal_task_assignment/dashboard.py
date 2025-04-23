import frappe
from frappe import _

@frappe.whitelist()
def get_maintenance_status_summary():
	return frappe.db.sql("""
		SELECT status, COUNT(*) as count
		FROM `tabAsset Maintenance Request`
		GROUP BY status
	""", as_dict=True)
