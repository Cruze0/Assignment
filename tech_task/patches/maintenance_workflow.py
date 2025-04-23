import frappe


def execute():
    """Create the 'Maintenance Request Approval Workflow' if it doesn’t exist."""
    wf_name = "Maintenance Request Approval"

    if frappe.db.exists("Workflow", wf_name):
        # already created, nothing to do
        return

    # ------------------------------------------------------------------
    # 1️⃣  Make sure the required roles exist
    # ------------------------------------------------------------------
    for role in ("Maintenance User", "Maintenance Team Supervisor"):
        if not frappe.db.exists("Role", role):
            frappe.get_doc(
                {"doctype": "Role", "role_name": role}
            ).insert(ignore_permissions=True)

    # ------------------------------------------------------------------
    # 2️⃣  Build the workflow document
    # ------------------------------------------------------------------
    workflow = frappe.get_doc(
        {
            "doctype": "Workflow",
            "workflow_name": wf_name,
            "document_type": "Asset Maintenance Request",
            "is_active": 1,
            "send_email_alert": 0,
            # this must be the Select field that stores your states
            "workflow_state_field": "status",
            # ---------- States (MUST match options in the status field) ----------
            "states": [
                {
                    "state": "Open",
                    "doc_status": 0,
                    "update_field": "status",
                    "allow_edit": "Maintenance User",
                },
                {
                    "state": "In Review",
                    "doc_status": 0,
                    "update_field": "status",
                    "allow_edit": "Maintenance Team Supervisor",
                },
                {
                    "state": "Completed",
                    "doc_status": 1,
                    "update_field": "status",
                    "allow_edit": "Maintenance Team Supervisor",
                },
            ],
            # ---------- Transition Rules ----------
            "transitions": [
                {
                    "action": "Submit for Review",
                    "state": "Open",
                    "next_state": "In Review",
                    "allowed": "Maintenance User",
                },
                {
                    "action": "Complete",
                    "state": "In Review",
                    "next_state": "Completed",
                    "allowed": "Maintenance Team Supervisor",
                },
                {
                    "action": "Reopen",
                    "state": "In Review",
                    "next_state": "Open",
                    "allowed": "Maintenance Team Supervisor",
                },
            ],
        }
    )

    workflow.insert(ignore_permissions=True)
    frappe.db.commit()
