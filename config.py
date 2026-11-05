"""
Configuration file for Alliance University Smart Campus Management System
Project: E1CSA313 Design Project - 1
Mentor: Dr. Vinita Nair
Module: Emergency & Notification Management
"""

import os

# Load environment variables from .env file (supports python-dotenv or native reader)
def _load_env_file():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass
    
    # Built-in fallback loader if python-dotenv is not installed
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        os.environ[k] = v
        except Exception:
            pass

_load_env_file()

# --- Alliance University Details ---
UNIVERSITY_NAME = "Alliance University"
ACCREDITATION = "NAAC Grade A+ Accredited University"
PROJECT_TITLE = "Smart Campus Management System Using AI"
COURSE_CODE = "E1CSA313 Design Project - 1"
MENTOR_NAME = "Dr. Vinita Nair"

# --- Supabase Credentials ---
# Students can set these in their .env file, in Streamlit secrets, or in the UI settings
DEFAULT_SUPABASE_URL = os.getenv("SUPABASE_URL", "https://icmnvizgjaqvraeitebz.supabase.co")
DEFAULT_SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# --- Campus Emergency Helplines ---
EMERGENCY_CONTACTS = [
    {
        "name": "Alliance Campus Security Control Room",
        "phone": "+91 80 4619 9000",
        "alt_phone": "Ext: 108",
        "desc": "24/7 Security patrol & emergency response team",
        "badge": "24/7 Priority"
    },
    {
        "name": "Campus Health & Medical Centre",
        "phone": "+91 80 4619 9112",
        "alt_phone": "Ext: 112",
        "desc": "On-campus doctors, nurses & first-aid ambulance",
        "badge": "Medical"
    },
    {
        "name": "Women's Safety & Harassment Cell",
        "phone": "+91 80 4619 9999",
        "alt_phone": "Toll Free: 1091",
        "desc": "Confidential quick assistance for female students & staff",
        "badge": "Confidential"
    },
    {
        "name": "National Emergency Helpline",
        "phone": "112",
        "alt_phone": "Police: 100 | Ambulance: 108",
        "desc": "All-in-one national emergency response",
        "badge": "National"
    },
    {
        "name": "Fire & Rescue Control",
        "phone": "101",
        "alt_phone": "Direct Fire Dispatch",
        "desc": "Emergency fire service station",
        "badge": "Fire"
    }
]

# --- Campus Locations at Alliance University ---
CAMPUS_LOCATIONS = [
    "Academic Block - Ground Floor",
    "Academic Block - 1st Floor (Computer Lab)",
    "Academic Block - 2nd Floor (Lecture Halls)",
    "Academic Block - 3rd Floor (Faculty Cabins)",
    "Central Library - Ground Floor",
    "Central Library - 1st Floor (Reading Hall)",
    "Administrative Block",
    "Food Court / Cafeteria",
    "Seminar Hall & Auditorium",
    "Student Activity Centre",
    "Hostel Block A (Boys Hostel)",
    "Hostel Block B (Girls Hostel)",
    "Alliance University Car Parking",
    "Sports Complex & Main Ground",
    "Main Entrance & Security Gate"
]

# --- Emergency Categories ---
EMERGENCY_TYPES = [
    "🚨 General Emergency / Threat",
    "🏥 Medical Emergency / Accident",
    "🔥 Fire Hazard / Smoke Alert",
    "🛡️ Physical Security / Violence",
    "🛑 Ragging / Harassment Alert",
    "⚡ Electrical / Infrastructure Hazard",
    "🧪 Chemical / Lab Hazard",
    "🌪️ Natural Disaster / Severe Weather"
]

# --- Evacuation Assembly Points ---
ASSEMBLY_POINTS = [
    "Central Lawn in front of Academic Block (Primary Assembly Area)",
    "Open Ground near Sports Complex",
    "Car Parking Area adjacent to Main Gate",
    "Basketball Court Area behind Hostel Block B"
]
