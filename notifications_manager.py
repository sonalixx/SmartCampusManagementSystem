"""
Notification and Emergency Management Business Logic
Coordinates SOS alerts, emergency incident reporting, notification filtering, and alerts.
"""

from typing import List, Dict, Any, Optional
import streamlit as st
from supabase_client import SupabaseManager
import config


class NotificationManager:
    def __init__(self, db: SupabaseManager):
        self.db = db

    def get_stats(self) -> Dict[str, int]:
        """Calculates total, unread, and active emergency counts."""
        notifs = self.db.fetch_notifications()
        total = len(notifs)
        unread = sum(1 for n in notifs if not n.get("is_read", False))
        emergencies = sum(1 for n in notifs if n.get("is_emergency") and n.get("status") == "active")
        return {
            "total": total,
            "unread": unread,
            "emergencies": emergencies
        }

    def filter_notifications(
        self,
        category: str = "All",
        status_filter: str = "All",
        search_query: str = ""
    ) -> List[Dict[str, Any]]:
        """Filters notifications based on user UI selections."""
        notifs = self.db.fetch_notifications()

        results = []
        for n in notifs:
            # Category filter
            if category == "🚨 Emergencies":
                if not n.get("is_emergency", False):
                    continue
            elif category == "📢 Announcements":
                if n.get("category") != "announcement":
                    continue
            elif category == "🛡️ Security":
                if n.get("category") != "security":
                    continue
            elif category == "🏥 Medical":
                if n.get("category") != "medical":
                    continue

            # Status filter
            if status_filter == "Unread Only" and n.get("is_read", False):
                continue
            elif status_filter == "Read Only" and not n.get("is_read", False):
                continue
            elif status_filter == "Active Emergencies":
                if not (n.get("is_emergency", False) and n.get("status") == "active"):
                    continue

            # Search query
            if search_query:
                q = search_query.lower()
                title_match = q in n.get("title", "").lower()
                msg_match = q in n.get("message", "").lower()
                sender_match = q in n.get("sender", "").lower()
                loc_match = q in n.get("location", "").lower()
                if not (title_match or msg_match or sender_match or loc_match):
                    continue

            results.append(n)

        return results

    def trigger_sos(
        self,
        student_name: str,
        student_id: str,
        location: str,
        emergency_type: str,
        contact_number: str = "Not Provided"
    ) -> Dict[str, Any]:
        """
        Instant Emergency SOS Trigger.
        Logs to database and creates a critical alert.
        """
        report = self.db.add_emergency_report(
            student_name=student_name,
            student_id=student_id,
            contact_number=contact_number,
            emergency_type=emergency_type,
            location=location,
            severity="Critical",
            description=f"CRITICAL SOS ACTIVATED by {student_name} ({student_id}) at {location}. Immediate assistance required!",
            status="Active"
        )
        return report

    def report_incident(
        self,
        student_name: str,
        student_id: str,
        contact_number: str,
        emergency_type: str,
        location: str,
        severity: str,
        description: str
    ) -> Dict[str, Any]:
        """Submits a formal emergency incident report."""
        report = self.db.add_emergency_report(
            student_name=student_name,
            student_id=student_id,
            contact_number=contact_number,
            emergency_type=emergency_type,
            location=location,
            severity=severity,
            description=description,
            status="Active"
        )
        return report


def render_audio_siren():
    """Generates an audible emergency beep/siren using Web Audio API in Streamlit."""
    audio_html = """
    <script>
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.4);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.4);
    } catch(e) {
        console.log("Audio alert blocked by browser autoplay policy", e);
    }
    </script>
    """
    st.components.v1.html(audio_html, height=0)

