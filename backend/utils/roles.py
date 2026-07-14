
class Role:
    ADMIN         = "ADMIN"
    STORE_MANAGER = "STORE_MANAGER"
    STORE_KEEPER  = "STORE_KEEPER"
    SITE MANAGER  = "SITE MANAGER"


ROLE_PERMISSIONS = {
    Role.ADMIN: [
        "manage_users",
        "manage_inventory",
        "manage_categories",
        "manage_events",
        "manage_job_cards",
        "dispatch_stock",
        "receive_stock",
        "return_stock",
        "report_damage",
        "view_reports",
        "view_dashboard"
    ],
    Role.STORE_MANAGER: [
        "manage_inventory",
        "manage_categories",
        "manage_events",
        "manage_job_cards",
        "dispatch_stock",
        "receive_stock",
        "return_stock",
        "report_damage",
        "view_reports",
        "view_dashboard"
    ],
    Role.STORE_KEEPER: [
        "manage_inventory",
        "receive_stock",
        "return_stock",
        "report_damage",
        "view_dashboard"
    ],
    Role.SITE MANAGER: [
        "view_dashboard",
        "manage_job_cards"
    ]
}