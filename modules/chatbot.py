"""
Alliance University - AI Campus Assistant & Management Module
Module 2: NLP Campus Chatbot, Occupancy Prediction & Issue Triage
Mentored by: Dr. Vinita Nair | E1CSA313 Design Project - 1
"""

import re
import datetime
from typing import List, Dict, Any, Optional, Tuple
from data.seed_data import AI_CAMPUS_KNOWLEDGE, PROJECT_METADATA, STUDENT_TEAM, CAMPUS_NODES


class CampusAI:
    """Intelligent Campus Assistant and Decision Support Engine."""

    def __init__(self):
        self.knowledge_base = AI_CAMPUS_KNOWLEDGE

    def answer_query(self, query: str) -> Dict[str, Any]:
        """
        Processes a natural language student query and returns the most
        relevant campus facility, schedule, contacts, and recommendations.
        """
        clean_q = query.lower().strip()
        words = re.findall(r"\b\w+\b", clean_q)

        # 1. Check for Project, Team or Mentor queries
        if any(w in clean_q for w in ["mentor", "vinita", "guide"]):
            return {
                "matched": True,
                "confidence": 0.99,
                "title": f"Project Mentor: {PROJECT_METADATA['mentor']}",
                "body": (
                    f"**{PROJECT_METADATA['mentor']}** is the Faculty Mentor for the "
                    f"**{PROJECT_METADATA['title']}** under course **{PROJECT_METADATA['course']}** "
                    f"at Alliance University."
                ),
                "location": "Department of Computer Science & Engineering, Faculty Chambers",
                "timings": "Office Hours: Mon - Fri (2:00 PM - 4:00 PM)",
                "contact": "vinita.nair@alliance.edu.in",
                "action_link": "Campus Navigation -> Destination: Academic Block - 3rd Floor (Faculty Cabins)"
            }

        if any(w in clean_q for w in ["team", "who made", "author", "students", "developer", "members", "bhavishya", "vidhyasri", "samriddhi", "dharshini"]):
            team_str = "\n".join([f"- **{m['name']}** ({m['id']}) — *{m['role']}*" for m in STUDENT_TEAM])
            return {
                "matched": True,
                "confidence": 0.98,
                "title": f"Project Team Members ({PROJECT_METADATA['university']})",
                "body": (
                    f"This project was designed and built by the CSE Student Research Team:\n\n{team_str}\n\n"
                    f"**Course:** {PROJECT_METADATA['course']} | **Mentor:** {PROJECT_METADATA['mentor']}"
                ),
                "location": "Alliance University, Anekal Main Road, Bengaluru",
                "timings": "Academic Session: 2026-2027",
                "contact": "cseteam@alliance.edu.in",
                "action_link": "Front Page -> Student Team Section"
            }

        # 2. Greetings & General Inquiries
        if any(clean_q.startswith(g) for g in ["hi", "hello", "hey", "good morning", "good afternoon"]):
            return {
                "matched": True,
                "confidence": 0.95,
                "title": "Welcome to Alliance University AI Assistant! 👋",
                "body": (
                    "Hello! I am your AI Campus Guide. I can help you find classrooms, computer labs, "
                    "library resources, fee inquiries, dining options, exam schedules, hostel facilities, "
                    "or assist with emergency SOS protocols. How may I assist you today?"
                ),
                "location": "Alliance University Smart Campus",
                "timings": "24/7 Available",
                "contact": "Ext: 100",
                "action_link": None
            }

        # 3. Knowledge Base Keyword & Semantic Search
        best_match = None
        highest_score = 0

        for item in self.knowledge_base:
            score = 0
            for kw in item["keywords"]:
                if kw in clean_q:
                    score += 2
                elif any(kw in w for w in words):
                    score += 1

            if score > highest_score:
                highest_score = score
                best_match = item

        if best_match and highest_score > 0:
            confidence = min(0.98, 0.60 + (highest_score * 0.12))
            return {
                "matched": True,
                "confidence": confidence,
                "title": f"Relevant Result: {best_match['facility']}",
                "body": best_match["details"],
                "location": best_match["location"],
                "timings": best_match["timings"],
                "contact": best_match["contact"],
                "action_link": best_match.get("action_link")
            }

        # 4. Fallback response with helpful guidance
        return {
            "matched": False,
            "confidence": 0.25,
            "title": "Campus Information Query",
            "body": (
                f"I couldn't find an exact match for '{query}'. "
                "You can ask about:\n"
                "- 📚 *'Where can I find books and journals?'*\n"
                "- 💻 *'Where can I find computer laboratories?'*\n"
                "- 💰 *'Where do I enquire about semester fees?'*\n"
                "- 🍽️ *'Where is the cafeteria / food court?'*\n"
                "- 🏥 *'How do I reach the health centre?'*\n"
                "- 🏨 *'What are the hostel curfew rules?'*"
            ),
            "location": "Student Helpdesk, Academic Block Ground Floor",
            "timings": "Mon - Sat: 9:00 AM - 5:00 PM",
            "contact": "General Helpdesk: +91 80 4619 9000",
            "action_link": "Campus Navigation -> Destination: Academic Block - Ground Floor"
        }

    @staticmethod
    def predict_room_occupancy(
        room_name: str,
        day_of_week: Optional[str] = None,
        hour_24: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Simulates ML-based classroom and lab occupancy prediction
        (Referenced in PPT Architecture Diagram: Module 2).
        """
        now = datetime.datetime.now()
        day = day_of_week or now.strftime("%A")
        hour = hour_24 if hour_24 is not None else now.hour

        # Peak hours: 10:00 to 16:00 on weekdays
        is_weekend = day in ["Saturday", "Sunday"]
        if is_weekend:
            occupancy_pct = 15
            status = "Vacant / Open for Study"
            color = "#10b981"
        elif 9 <= hour <= 12:
            occupancy_pct = 85
            status = "High Occupancy (Active Lecture/Lab)"
            color = "#ef4444"
        elif 13 <= hour <= 16:
            occupancy_pct = 70
            status = "Moderate Occupancy (Practical Sessions)"
            color = "#f59e0b"
        elif 17 <= hour <= 20:
            occupancy_pct = 30
            status = "Low Occupancy (Self Study / Project Work)"
            color = "#10b981"
        else:
            occupancy_pct = 5
            status = "Closed / Off-Hours"
            color = "#64748b"

        return {
            "room": room_name,
            "day": day,
            "time_slot": f"{hour:02d}:00 - {(hour+1)%24:02d}:00",
            "predicted_occupancy_pct": occupancy_pct,
            "status": status,
            "color": color,
            "available_seats": max(0, round(60 * (1 - occupancy_pct / 100.0))),
            "total_capacity": 60
        }

    @staticmethod
    def triage_maintenance_issue(description: str) -> Dict[str, str]:
        """
        AI Issue Triage: Automatically classifies maintenance requests
        by category, urgency, and routing department.
        """
        desc_lower = description.lower()

        # Category detection
        if any(w in desc_lower for w in ["wire", "light", "fan", "switch", "power", "shock", "electric", "ac", "air condition"]):
            category = "Electrical"
            dept = "Electrical Maintenance Division"
            priority = "High" if any(w in desc_lower for w in ["spark", "smoke", "shock", "outage"]) else "Medium"
        elif any(w in desc_lower for w in ["water", "leak", "pipe", "tap", "sink", "cooler", "drain", "toilet", "washroom"]):
            category = "Plumbing"
            dept = "Water & Sanitation Division"
            priority = "High" if any(w in desc_lower for w in ["flood", "burst", "overflow"]) else "Medium"
        elif any(w in desc_lower for w in ["computer", "wifi", "internet", "projector", "screen", "keyboard", "lan", "hdmi"]):
            category = "IT / Equipment"
            dept = "Campus IT Systems Group"
            priority = "High" if "exam" in desc_lower or "lecture" in desc_lower else "Medium"
        elif any(w in desc_lower for w in ["clean", "dust", "garbage", "trash", "smell", "waste"]):
            category = "Cleanliness"
            dept = "Housekeeping & Facility Management"
            priority = "Medium"
        else:
            category = "General Infrastructure"
            dept = "Campus Estate Office"
            priority = "Medium"

        return {
            "category": category,
            "suggested_priority": priority,
            "assigned_department": dept,
            "triage_summary": f"Categorized as {category} with {priority} priority."
        }

