"""
Supabase Database Client for Smart Campus Management System
Handles online database storage via Supabase Cloud with automatic local fallback.
"""

import os
import json
import uuid
import datetime
from typing import List, Dict, Any, Optional, Tuple
import requests

LOCAL_DB_FILE = os.path.join(os.path.dirname(__file__), "campus_local_db.json")

# Default seed data matching Alliance University PPT slides
INITIAL_DATA = {
    "campus_notifications": [
        {
            "id": "1a2b3c4d-0001-4000-8000-000000000001",
            "title": "Seminar Announcement",
            "message": "A technical seminar will be conducted in the Seminar Hall.",
            "category": "announcement",
            "priority": "medium",
            "sender": "Department of Computer Science",
            "location": "Seminar Hall",
            "is_emergency": False,
            "is_read": False,
            "status": "active",
            "created_at": "2026-10-23 12:37:03"
        },
        {
            "id": "1a2b3c4d-0002-4000-8000-000000000002",
            "title": "Library Timings Update",
            "message": "The library will remain open until 8 PM today.",
            "category": "announcement",
            "priority": "low",
            "sender": "Central Library",
            "location": "Central Library",
            "is_emergency": False,
            "is_read": False,
            "status": "active",
            "created_at": "2026-10-23 10:15:00"
        },
        {
            "id": "1a2b3c4d-0003-4000-8000-000000000003",
            "title": "Campus Safety & First Aid Notice",
            "message": "Annual safety inspection and emergency team deployment across all blocks.",
            "category": "security",
            "priority": "medium",
            "sender": "Alliance Campus Security",
            "location": "Campus-wide",
            "is_emergency": False,
            "is_read": True,
            "status": "active",
            "created_at": "2026-10-22 09:00:00"
        }
    ],
    "emergency_reports": []
}


def _ensure_local_db() -> Dict[str, Any]:
    """Ensures local fallback storage exists and returns its contents."""
    if not os.path.exists(LOCAL_DB_FILE):
        try:
            with open(LOCAL_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(INITIAL_DATA, f, indent=2)
            return INITIAL_DATA
        except Exception:
            return INITIAL_DATA

    try:
        with open(LOCAL_DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "campus_notifications" not in data:
                data["campus_notifications"] = INITIAL_DATA["campus_notifications"]
            if "emergency_reports" not in data:
                data["emergency_reports"] = []
            return data
    except Exception:
        return INITIAL_DATA


def _save_local_db(data: Dict[str, Any]) -> None:
    """Saves data into local fallback JSON database."""
    try:
        with open(LOCAL_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving to local DB: {e}")


class SupabaseManager:
    def __init__(self, supabase_url: str = "", supabase_key: str = ""):
        self.url = (supabase_url or "").strip().rstrip("/")
        self.key = (supabase_key or "").strip()
        self.is_configured = bool(self.url and self.key and "supabase.co" in self.url)

    def get_headers(self) -> Dict[str, str]:
        """Headers required for PostgREST API access to Supabase."""
        return {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def test_connection(self) -> Tuple[bool, str]:
        """Tests whether connection to Supabase cloud is live and working."""
        if not self.is_configured:
            return False, "Supabase credentials are not set (Using Local Offline Storage)."

        try:
            endpoint = f"{self.url}/rest/v1/campus_notifications?select=id&limit=1"
            resp = requests.get(endpoint, headers=self.get_headers(), timeout=5)
            if resp.status_code in [200, 206]:
                return True, f"Connected to Supabase Cloud ({self.url})"
            elif resp.status_code == 401:
                return False, "Authentication Error: Invalid API key."
            elif resp.status_code == 404:
                return False, "Table 'campus_notifications' not found. Please run schema.sql in Supabase SQL Editor."
            else:
                return False, f"Supabase responded with HTTP {resp.status_code}: {resp.text[:120]}"
        except requests.exceptions.RequestException as e:
            return False, f"Network/Connection error: {str(e)[:120]}"

    # --- NOTIFICATIONS METHODS ---

    def fetch_notifications(self) -> List[Dict[str, Any]]:
        """Fetches all notifications from Supabase, or local storage if offline."""
        if self.is_configured:
            try:
                endpoint = f"{self.url}/rest/v1/campus_notifications?select=*&order=created_at.desc"
                resp = requests.get(endpoint, headers=self.get_headers(), timeout=6)
                if resp.status_code == 200:
                    return resp.json()
            except Exception as e:
                print(f"Failed to fetch from Supabase cloud: {e}. Falling back to local storage.")

        # Fallback to local
        data = _ensure_local_db()
        items = list(data.get("campus_notifications", []))
        items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return items

    def add_notification(
        self,
        title: str,
        message: str,
        category: str = "announcement",
        priority: str = "medium",
        sender: str = "Campus Administration",
        location: str = "Campus-wide",
        is_emergency: bool = False,
        status: str = "active"
    ) -> Dict[str, Any]:
        """Adds a new notification to Supabase (or local fallback)."""
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "id": str(uuid.uuid4()),
            "title": title,
            "message": message,
            "category": category,
            "priority": priority,
            "sender": sender,
            "location": location,
            "is_emergency": is_emergency,
            "is_read": False,
            "status": status,
            "created_at": now_str
        }

        if self.is_configured:
            try:
                endpoint = f"{self.url}/rest/v1/campus_notifications"
                resp = requests.post(endpoint, headers=self.get_headers(), json=record, timeout=6)
                if resp.status_code in [200, 201]:
                    results = resp.json()
                    if results and isinstance(results, list):
                        return results[0]
                    return record
            except Exception as e:
                print(f"Error inserting into Supabase: {e}. Saving locally.")

        # Save locally
        data = _ensure_local_db()
        data["campus_notifications"].insert(0, record)
        _save_local_db(data)
        return record

    def mark_notification_as_read(self, notification_id: str, is_read: bool = True) -> bool:
        """Marks a notification as read or unread."""
        if self.is_configured:
            try:
                endpoint = f"{self.url}/rest/v1/campus_notifications?id=eq.{notification_id}"
                resp = requests.patch(endpoint, headers=self.get_headers(), json={"is_read": is_read}, timeout=5)
                if resp.status_code in [200, 204]:
                    return True
            except Exception:
                pass

        # Update locally
        data = _ensure_local_db()
        for item in data.get("campus_notifications", []):
            if str(item.get("id")) == str(notification_id):
                item["is_read"] = is_read
                _save_local_db(data)
                return True
        return False

    def mark_all_notifications_as_read(self) -> bool:
        """Marks all notifications as read."""
        if self.is_configured:
            try:
                endpoint = f"{self.url}/rest/v1/campus_notifications?is_read=eq.false"
                resp = requests.patch(endpoint, headers=self.get_headers(), json={"is_read": True}, timeout=6)
                if resp.status_code in [200, 204]:
                    return True
            except Exception:
                pass

        # Update locally
        data = _ensure_local_db()
        for item in data.get("campus_notifications", []):
            item["is_read"] = True
        _save_local_db(data)
        return True

    def delete_notification(self, notification_id: str) -> bool:
        """Deletes a notification by ID."""
        if self.is_configured:
            try:
                endpoint = f"{self.url}/rest/v1/campus_notifications?id=eq.{notification_id}"
                resp = requests.delete(endpoint, headers=self.get_headers(), timeout=5)
                if resp.status_code in [200, 204]:
                    return True
            except Exception:
                pass

        # Delete locally
        data = _ensure_local_db()
        original_len = len(data.get("campus_notifications", []))
        data["campus_notifications"] = [
            n for n in data.get("campus_notifications", [])
            if str(n.get("id")) != str(notification_id)
        ]
        if len(data["campus_notifications"]) != original_len:
            _save_local_db(data)
            return True
        return False

    def clear_all_notifications(self) -> bool:
        """Clears all notifications."""
        if self.is_configured:
            try:
                endpoint = f"{self.url}/rest/v1/campus_notifications?id=neq.00000000-0000-0000-0000-000000000000"
                resp = requests.delete(endpoint, headers=self.get_headers(), timeout=6)
                if resp.status_code in [200, 204]:
                    return True
            except Exception:
                pass

        data = _ensure_local_db()
        data["campus_notifications"] = []
        _save_local_db(data)
        return True

    # --- EMERGENCY REPORTS & SOS METHODS ---

    def add_emergency_report(
        self,
        student_name: str,
        student_id: str,
        contact_number: str,
        emergency_type: str,
        location: str,
        severity: str = "Critical",
        description: str = "",
        status: str = "Active"
    ) -> Dict[str, Any]:
        """Saves an emergency report / SOS incident to Supabase."""
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_id = str(uuid.uuid4())

        # Also create a high-priority Campus Notification for this emergency so it displays everywhere
        emergency_title = f"🚨 {emergency_type.upper()} AT {location.upper()}"
        emergency_msg = (
            f"REPORTED BY: {student_name} (ID: {student_id}). "
            f"Severity: {severity}. {description}. Emergency teams dispatched!"
        )
        notif = self.add_notification(
            title=emergency_title,
            message=emergency_msg,
            category="emergency",
            priority="critical" if severity == "Critical" else "high",
            sender=f"SOS Alert - {student_name}",
            location=location,
            is_emergency=True,
            status="active"
        )

        record = {
            "id": report_id,
            "notification_id": notif.get("id"),
            "student_name": student_name,
            "student_id": student_id,
            "contact_number": contact_number,
            "emergency_type": emergency_type,
            "location": location,
            "severity": severity,
            "description": description or f"Emergency reported at {location} by {student_name}",
            "status": status,
            "created_at": now_str
        }

        if self.is_configured:
            try:
                endpoint = f"{self.url}/rest/v1/emergency_reports"
                resp = requests.post(endpoint, headers=self.get_headers(), json=record, timeout=6)
                if resp.status_code in [200, 201]:
                    results = resp.json()
                    if results and isinstance(results, list):
                        return results[0]
                    return record
            except Exception as e:
                print(f"Error inserting emergency report to Supabase: {e}")

        # Local fallback
        data = _ensure_local_db()
        data["emergency_reports"].insert(0, record)
        _save_local_db(data)
        return record

    def fetch_emergency_reports(self) -> List[Dict[str, Any]]:
        """Fetches all emergency reports."""
        if self.is_configured:
            try:
                endpoint = f"{self.url}/rest/v1/emergency_reports?select=*&order=created_at.desc"
                resp = requests.get(endpoint, headers=self.get_headers(), timeout=6)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass

        data = _ensure_local_db()
        reports = list(data.get("emergency_reports", []))
        reports.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return reports

    def get_active_emergency(self) -> Optional[Dict[str, Any]]:
        """Checks if there is any active, unresolved emergency alert."""
        # First check notifications for active emergency
        notifs = self.fetch_notifications()
        for n in notifs:
            if n.get("is_emergency") and n.get("status") == "active":
                return n
        # Check reports
        reports = self.fetch_emergency_reports()
        for r in reports:
            if r.get("status") == "Active":
                return {
                    "id": r.get("id"),
                    "title": f"🚨 {r.get('emergency_type')} ALERT",
                    "message": r.get("description"),
                    "location": r.get("location"),
                    "severity": r.get("severity"),
                    "created_at": r.get("created_at"),
                    "is_emergency": True
                }
        return None

    def resolve_emergency(self, emergency_id: str) -> bool:
        """Marks an emergency and its associated notifications as resolved."""
        data = _ensure_local_db()
        linked_notif_ids = set()
        
        # Check emergency reports to find matching and linked ids
        for item in data.get("emergency_reports", []):
            if str(item.get("id")) == str(emergency_id) or str(item.get("notification_id")) == str(emergency_id):
                item["status"] = "Resolved"
                if item.get("notification_id"):
                    linked_notif_ids.add(str(item.get("notification_id")))

        # Check notifications
        for item in data.get("campus_notifications", []):
            if str(item.get("id")) == str(emergency_id) or str(item.get("id")) in linked_notif_ids:
                item["status"] = "resolved"

        # If it was an emergency notification itself, also mark all other active emergency notifications resolved if desired
        if not emergency_id:
            for item in data.get("campus_notifications", []):
                if item.get("is_emergency"):
                    item["status"] = "resolved"

        _save_local_db(data)

        # Update in Supabase cloud if connected
        if self.is_configured:
            try:
                requests.patch(
                    f"{self.url}/rest/v1/campus_notifications?id=eq.{emergency_id}",
                    headers=self.get_headers(),
                    json={"status": "resolved"},
                    timeout=5
                )
                requests.patch(
                    f"{self.url}/rest/v1/emergency_reports?id=eq.{emergency_id}",
                    headers=self.get_headers(),
                    json={"status": "Resolved"},
                    timeout=5
                )
                for nid in linked_notif_ids:
                    requests.patch(
                        f"{self.url}/rest/v1/campus_notifications?id=eq.{nid}",
                        headers=self.get_headers(),
                        json={"status": "resolved"},
                        timeout=5
                    )
            except Exception:
                pass

        return True
