"""
Alliance University - Database Queries & Access Layer
Provides query helper utilities for Supabase PostgREST & local persistence.
"""

from typing import List, Dict, Any, Optional
import os
import json

LOCAL_DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "campus_local_db.json")

# SQL Schema Constants
CREATE_NOTIFICATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS public.campus_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'announcement',
    priority TEXT NOT NULL DEFAULT 'medium',
    sender TEXT NOT NULL DEFAULT 'Campus Administration',
    location TEXT DEFAULT 'Campus-wide',
    is_emergency BOOLEAN DEFAULT FALSE,
    is_read BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

CREATE_EMERGENCY_REPORTS_TABLE = """
CREATE TABLE IF NOT EXISTS public.emergency_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    emergency_type TEXT NOT NULL,
    location TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'Critical',
    description TEXT,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

CREATE_MAINTENANCE_TICKETS_TABLE = """
CREATE TABLE IF NOT EXISTS public.maintenance_tickets (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    location TEXT NOT NULL,
    reported_by TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'Medium',
    status TEXT NOT NULL DEFAULT 'Submitted',
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""


def load_maintenance_tickets() -> List[Dict[str, Any]]:
    """Loads maintenance tickets from local database or seed defaults."""
    if os.path.exists(LOCAL_DB_FILE):
        try:
            with open(LOCAL_DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "maintenance_tickets" in data:
                    return data["maintenance_tickets"]
        except Exception:
            pass
    from data.seed_data import SAMPLE_MAINTENANCE_TICKETS
    return list(SAMPLE_MAINTENANCE_TICKETS)


def save_maintenance_ticket(ticket: Dict[str, Any]) -> bool:
    """Appends a new maintenance ticket to persistent storage."""
    try:
        data = {}
        if os.path.exists(LOCAL_DB_FILE):
            with open(LOCAL_DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        tickets = data.get("maintenance_tickets", [])
        tickets.insert(0, ticket)
        data["maintenance_tickets"] = tickets

        with open(LOCAL_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving maintenance ticket: {e}")
        return False

