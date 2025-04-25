# Tech Task: Asset Maintenance Request

This is a custom Frappe app for managing Asset Maintenance Requests.

---

## Task 1: Custom Doctype – Asset Maintenance Request

Create a new Doctype named **"Asset Maintenance Request"** to manage maintenance requests for company assets.

### 🔧 Fields to Include:

| Field Label                | Field Type  | Notes                                                                 |
|---------------------------|-------------|-----------------------------------------------------------------------|
| Request Date              | Date        | Default to current date                                              |
| Asset                     | Link        | Link to the **Asset** Doctype                                        |
| Asset Name                | Data        | Auto-fetch from selected Asset                                       |
| Maintenance Type          | Select      | Options: Preventive, Corrective, Emergency                           |
| Requested By              | Link        | Link to the **Employee** Doctype                                     |
| Employee Name             | Data        | Auto-fetch from selected "Requested By"                              |
| Department                | Link        | Auto-fetch from selected Employee                                    |
| Priority                  | Select      | Options: Low, Medium, High, Urgent                                   |
| Expected Completion Date  | Date        |                                                                       |
| Resolution Time (Hours)   | Float       |                                                                       |
| Status                    | Select      | Options: Open, In Progress, In Review, Completed                     |

Make sure to configure the auto-fetching using "Fetch From" property or through client scripting if needed.

---

## Task 2: Customization and Logic

### ✅ 1. Filter Asset Field to Only Show "In Use" Assets
To ensure that the `Asset` link field only shows assets with the status `"In Use"`, follow these steps:

#### ➤ Add "In Use" as an option in the **status** field of the **Asset** Doctype:
1. Go to **Asset** Doctype (`/app/doctype/asset`).
2. Find the **status** field.
3. Add `"In Use"` to the list of options if it's not already there.


## Task 3: Button and Navigation
### Create Maintenance Task Button:
1. Add a button labeled "Create Maintenance Task" visible only after the document is saved and will be visible to the Maintenance Team Supervisor(role-based).
2. When clicked, the button should create a new Task in the "Project" module, linking it to the selected asset.(create custom fields in Task as required) and the Maintenance Team Supervisor(role-based) will assign the task to Maintenance Team member (using assign to) and Update Status to in-Progress in Asset Maintenance Request.
3. The created Task should inherit these details from the Asset Maintenance Request:
   Subject Should be (Asset Name-Maintenance Type-series)
   Expected Completion Date
   Priority
4. When the Task is Set to Completed by a Maintenance Team member,calculate the time difference between Request Date and Expected Completion Date and update the  Resolution Time field in Asset maintenance Request and update Status of Asset Maintenance Request to "In Review"


## Task 4: Custom Workflow
### Maintenance Request Approval Workflow:
1. Create a workflow such that when the Status  can be set to "Completed" only by the Maintenance Team Supervisor.
### NOTE: for creating and executing workflow just follow this steps
1. Open Python console: bench --site site-name console
2. run this command for workflow: import tech_task.patches.maintenance_workflow as patch
3. and then patch.execute()
4. and for "Maintenance Team" and "Maintenance Team Supervisor" role (automatic Role Allocatio to Administrator)
5. run this command for role allocation to Administrator: import tech_task.patches.assign_roles_to_admin as patch
6. and then patch.execute()

### NOTE: Task 5 i have done through Page

## Task 5: Reporting and Dashboard
1. Maintenance Dashboard:
2. Create a dashboard widget that shows:
3. Total number of open requests.
4. Total number of critical priority requests.
5. Pie chart of maintenance requests based on status


## Task 6: Print Format Issue Resolution
1.  Investigate why the item description in a child table overlaps with the table heading on the next page when it exceeds one page. (You can use the print format of any Doctype that has an Items table).  
2. Modify the standard print format to ensure that long descriptions are handled correctly. Specifically, ensure:  
   - The item description wraps across multiple lines.  
   - There is no overlap with the table heading on the next page.  
   - The print format remains clear and professional, even when the description spans multiple pages.  
3. Provide a detailed explanation of how you solved the issue, including any code or changes made to the print format. 



### for Task 6 i have a attched a document of Quality Inspection Template doctype here you can see the header is not overlapping with child table
i have used this css

.header-space1, .footer-space1 {
    height: 195px;
    width: 97%;
  }
.fixed-table-header {
      position: fixed;
      top: 180px;
      width: 100%;
      z-index: 100;
      display: table-header-group;
    }
    .fixed-table-header:not(:first-of-type) {
      page-break-before: always;
    }


