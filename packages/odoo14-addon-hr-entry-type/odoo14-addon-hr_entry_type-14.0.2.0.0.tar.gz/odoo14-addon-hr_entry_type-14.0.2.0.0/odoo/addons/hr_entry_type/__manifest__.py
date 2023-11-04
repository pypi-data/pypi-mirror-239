# trunk-ignore(ruff/B018)
{
    "name": "HR Attendance Entry Types",
    "license": "AGPL-3",
    "version": "14.0.2.0.0",
    "category": "Human Resources",
    "sequence": 20,
    "summary": "Entry Types to Employee Attendances",
    "website": "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/odoo-mitxelena",
    "description": """
        This module adds the possibility to add entry types to employee attendances. 
        This will be used to define the corrective factor for each entry type's extra hours.

        It also adds the possibility to define if the entire time of every kind of entry is extra time or not.

        It depends on the module hr_attendance only for the menu entry.
    """,
    "author": "Coopdevs Treball SCCL",
    "depends": [
        "base",
        "hr_attendance",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_entry_type_views.xml",
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
