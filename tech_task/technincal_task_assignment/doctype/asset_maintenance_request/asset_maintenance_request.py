# Copyright (c) 2025, Ankit and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.desk.form.assign_to import add as assign_to_user
from frappe.share import add as add_assignment
from frappe.utils import get_datetime, time_diff_in_hours
from frappe.utils import get_url

class AssetMaintenanceRequest(Document):
    pass
    # def after_save(self):
    #     print(">>> After save hit")
    #     frappe.msgprint("After save function triggered.")
    #     if self.priority == "Urgent":
    #         self.send_urgent_email()

    # def send_urgent_email(self):
    #     supervisors = frappe.get_all(
    #         "Has Role",
    #         filters={"role": "Maintenance Team Supervisor"},
    #         fields=["parent"]
    #     )

    #     recipient_emails = [
    #         frappe.db.get_value("User", user.parent, "email")
    #         for user in supervisors
    #         if frappe.db.get_value("User", user.parent, "enabled")
    #     ]
    #     recipient_emails = list(filter(None, recipient_emails))

    #     if recipient_emails:
    #         sender_email = "ankit.m0720@gmail.com"
    #         subject = f"[Urgent] Maintenance Request: {self.asset_name or self.asset}"
    #         link = f"{get_url()}/app/asset-maintenance-request/{self.name}"
    #         message = f"""
    #             <p><strong>An <span style="color:red;">urgent</span> maintenance request has been submitted.</strong></p>
    #             <p><b>Asset:</b> {self.asset or ''} - {self.asset_name or ''}</p>
    #             <p><b>Requested By:</b> {self.requested_by or ''} - {self.employee_name or ''}</p>
    #             <p><b>Expected Completion Date:</b> {self.expected_completion_date or 'Not Set'}</p>
    #             <p><b>Priority:</b> {self.priority}</p>
    #             <p><a href="{link}">Click here to view the Maintenance Request</a></p>
    #             <br/>
    #             <p>Regards,<br>{frappe.utils.get_fullname(frappe.session.user)}</p>
    #         """

    #         frappe.sendmail(
    #             recipients=recipient_emails,
    #             sender=sender_email,
    #             subject=subject,
    #             message=message,
    #             reference_doctype=self.doctype,
    #             reference_name=self.name
    #         )
    #         frappe.msgprint("Urgent email sent to Maintenance Team Supervisors.")







@frappe.whitelist()
def create_maintenance_task(docname):
    doc = frappe.get_doc("Asset Maintenance Request", docname)

    if not doc.asset or not doc.asset_name:
        frappe.throw(_("Asset and Asset Name are required to create a Maintenance Task."))

    task_subject = f"{doc.asset_name}-{doc.maintenance_type}-{doc.name}"

    # Create new Task
    task = frappe.new_doc("Task")
    task.subject = task_subject
    task.expected_start_date = doc.request_date
    task.exp_end_date = doc.expected_completion_date
    task.priority = doc.priority
    task.status = "Open"

    # Map to custom fields in Task
    task.custom_asset = doc.asset
    task.custom_asset_maintenance_request = doc.name

    task.insert(ignore_permissions=True)

    # Assign to Maintenance Team member
    maintenance_team_users = frappe.get_all(
        "Has Role",
        filters={"role": "Maintenance Team"},
        fields=["parent"]
    )

    if maintenance_team_users:
        assignee = maintenance_team_users[0].parent
        assign_to_user({
            "doctype": "Task",
            "name": task.name,
            "assign_to": [assignee],
            "description": f"Assigned from Asset Maintenance Request: {doc.name}"
        })

    # Update status of Asset Maintenance Request
    doc.db_set("status", "In Progress")

    frappe.msgprint(_("Maintenance Task {0} created and assigned to {1}").format(task.name, assignee))
    return task.name



# Hook for Task update (this should be called via hooks.py or event)
def on_task_update(doc, method):
    if doc.status == "Completed" and doc.custom_asset_maintenance_request:
        try:
            maintenance_doc = frappe.get_doc("Asset Maintenance Request", doc.custom_asset_maintenance_request)
            resolution_hours = time_diff_in_hours(get_datetime(), maintenance_doc.request_date)
            maintenance_doc.db_set("resolution_time_hours", resolution_hours)
            maintenance_doc.db_set("status", "In Review")
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Error updating Asset Maintenance Request on Task completion")
