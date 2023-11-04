# trunk-ignore(ruff/B018)
{
    "name": "HR Attendance Mitxelena Entry Types",
    "license": "AGPL-3",
    "version": "14.0.1.0.0",
    "category": "Human Resources",
    "sequence": 20,
    "summary": "Entry Types to Employee Attendances Customizations for Mitxelena",
    "website": "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/odoo-mitxelena",
    "author": "Coopdevs Treball SCCL",
    "depends": [
        "base",
    ],
    "data": [
        "data/hr_entry_type.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
