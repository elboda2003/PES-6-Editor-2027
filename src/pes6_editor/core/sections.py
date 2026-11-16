"""Single source of truth for application sections and their status."""

SECTIONS = (
    {
        "id": "dashboard",
        "title": "Dashboard",
        "status": "Available — tool status overview",
        "enabled": True,
    },
    {
        "id": "file_browser",
        "title": "File Browser",
        "status": "Available — read-only file inspection",
        "enabled": True,
    },
    {
        "id": "afs_inspector",
        "title": "AFS Inspector",
        "status": "Available — signature check; entry layout unverified",
        "enabled": True,
    },
    {
        "id": "players",
        "title": "Players",
        "status": "Not implemented — editing unavailable",
        "enabled": False,
    },
    {
        "id": "teams",
        "title": "Teams",
        "status": "Not implemented — editing unavailable",
        "enabled": False,
    },
    {
        "id": "transfers",
        "title": "Transfers",
        "status": "Not implemented — editing unavailable",
        "enabled": False,
    },
    {
        "id": "competitions",
        "title": "Competitions",
        "status": "Not implemented — editing unavailable",
        "enabled": False,
    },
    {
        "id": "stadiums",
        "title": "Stadiums",
        "status": "Not implemented — editing unavailable",
        "enabled": False,
    },
    {
        "id": "graphics",
        "title": "Graphics",
        "status": "Not implemented — editing unavailable",
        "enabled": False,
    },
    {
        "id": "settings",
        "title": "Settings",
        "status": "Available — compatibility and safety information",
        "enabled": True,
    },
)

SECTION_BY_ID = {section["id"]: section for section in SECTIONS}
