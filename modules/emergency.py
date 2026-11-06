"""
Alliance University - Emergency Services Module
Module 3: Centralized Campus & Emergency Services
Mentored by: Dr. Vinita Nair | E1CSA313 Design Project - 1
"""

import datetime
from typing import List, Dict, Any, Optional
from supabase_client import SupabaseManager
import config


class EmergencySystem:
    """Enterprise campus emergency and safety orchestration service."""

    def __init__(self, db: SupabaseManager):
        self.db = db

    def dispatch_sos(
        self,
        student_name: str,
        student_id: str,
        location: str,
        emergency_type: str,
        contact_number: str = "+91 80 4619 9000"
    ) -> Dict[str, Any]:
        """Dispatches an instant emergency alert across campus screens and database."""
        report = self.db.add_emergency_report(
            student_name=student_name,
            student_id=student_id,
            contact_number=contact_number,
            emergency_type=emergency_type,
            location=location,
            severity="Critical",
            description=f"CRITICAL DISTRESS SIGNAL emitted by {student_name} ({student_id}) at {location}. Immediate team dispatch requested.",
            status="Active"
        )
        return report

    def submit_detailed_report(
        self,
        student_name: str,
        student_id: str,
        contact_number: str,
        emergency_type: str,
        location: str,
        severity: str,
        description: str
    ) -> Dict[str, Any]:
        """Submits a comprehensive safety report with witness tracking and severity."""
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

    def resolve_emergency(self, emergency_id: str) -> bool:
        """Marks an active emergency as resolved and deactivates sirens/popups."""
        return self.db.resolve_emergency(emergency_id)

    def get_evacuation_guidelines(self) -> List[Dict[str, str]]:
        """Standard Operating Procedures for campus safety and fire evacuation."""
        return [
            {
                "step": "1. Stay Calm & Alert",
                "instruction": "Cease work immediately, leave non-essential personal belongings, and remain calm."
            },
            {
                "step": "2. Never Use Elevators",
                "instruction": "Always use designated emergency fire stairwells. Elevators may experience sudden power loss."
            },
            {
                "step": "3. Proceed to Safe Assembly Point",
                "instruction": "Evacuate swiftly to Central Lawn in front of Academic Block or Open Ground near Sports Complex."
            },
            {
                "step": "4. Assist & Report",
                "instruction": "Assist injured individuals or people with disabilities. Report roll-call to Campus Safety Wardens."
            }
        ]

