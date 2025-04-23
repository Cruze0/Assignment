// Copyright (c) 2025, Ankit and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Asset Maintenance Request", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Asset Maintenance Request', {
    onload: function(frm) {
        // Set filter on Asset field to only show assets with status "In Use"
        frm.set_query("asset", () => {
            return {
                filters: {
                    status: "In Use"
                }
            };
        });
    },

    refresh: function(frm) {
        // Show "Create Maintenance Task" button only if document is saved and user has the role
        if (!frm.is_new() && frappe.user.has_role("Maintenance Team Supervisor")) {
            frm.add_custom_button("Create Maintenance Task", function () {
                frappe.call({
                    method: "tech_task.technincal_task_assignment.doctype.asset_maintenance_request.asset_maintenance_request.create_maintenance_task",
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__("Task Created: <a href='/app/task/" + r.message + "'>" + r.message + "</a>"), __("Success"));
                        }
                    }
                });
            });
        }
    }
});

