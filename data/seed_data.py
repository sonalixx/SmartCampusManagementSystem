"""
Alliance University - Smart Campus Management System
Seed Data & Campus Knowledge Base
Course: E1CSA313 Design Project - 1
Mentor: Dr. Vinita Nair
"""

# ==============================================================================
# 1. STUDENT TEAM & PROFILES
# ==============================================================================
STUDENT_TEAM = [
    {
        "name": "Bhavishya Raj M.H",
        "id": "2411021060805",
        "role": "Team Lead & Full-Stack Developer",
        "email": "bhavishya.2411021060805@alliance.edu.in",
        "department": "Computer Science & Engineering",
        "semester": "5th Semester - B.Tech CSE",
        "attendance": "96.4%",
        "cgpa": "9.24",
        "enrolled_credits": 24,
        "avatar": "👨‍🎓"
    },
    {
        "name": "Vidhyasri. R",
        "id": "2411021060047",
        "role": "AI / ML & Database Specialist",
        "email": "vidhyasri.2411021060047@alliance.edu.in",
        "department": "Computer Science & Engineering",
        "semester": "5th Semester - B.Tech CSE",
        "attendance": "94.8%",
        "cgpa": "9.18",
        "enrolled_credits": 24,
        "avatar": "👩‍🎓"
    },
    {
        "name": "Samriddhi Singh",
        "id": "2411021060838",
        "role": "System Architecture & Navigation Engineer",
        "email": "samriddhi.2411021060838@alliance.edu.in",
        "department": "Computer Science & Engineering",
        "semester": "5th Semester - B.Tech CSE",
        "attendance": "93.5%",
        "cgpa": "8.95",
        "enrolled_credits": 24,
        "avatar": "👩‍🎓"
    },
    {
        "name": "R. Dharshini",
        "id": "2411021060087",
        "role": "Emergency Systems & UI/UX Developer",
        "email": "dharshini.2411021060087@alliance.edu.in",
        "department": "Computer Science & Engineering",
        "semester": "5th Semester - B.Tech CSE",
        "attendance": "95.2%",
        "cgpa": "9.05",
        "enrolled_credits": 24,
        "avatar": "👩‍🎓"
    }
]

PROJECT_METADATA = {
    "title": "Smart Campus Management System Using AI",
    "course": "E1CSA313 Design Project - 1",
    "mentor": "Dr. Vinita Nair",
    "university": "Alliance University",
    "accreditation": "NAAC Grade A+ Accredited University",
    "academic_year": "2026-2027",
    "version": "2.4.0 (Enterprise Gold)",
    "description": (
        "A comprehensive AI-powered smart campus operating platform integrating "
        "A*/Dijkstra campus navigation, an intelligent campus virtual assistant, "
        "and centralized emergency response with Supabase cloud persistence."
    )
}

# ==============================================================================
# 2. CAMPUS NAVIGATION GRAPH & POINTS OF INTEREST (POI)
# ==============================================================================
CAMPUS_NODES = {
    "Main Entrance & Security Gate": {
        "x": 120, "y": 300, "category": "Administrative", "floor": "Ground",
        "description": "Primary university entry gate with visitor pass verification and 24/7 security booth."
    },
    "Alliance University Car Parking": {
        "x": 220, "y": 140, "category": "Facilities", "floor": "Ground",
        "description": "Multi-tier parking facility for student two-wheelers, faculty, and visitor vehicles."
    },
    "Administrative Block": {
        "x": 340, "y": 280, "category": "Administrative", "floor": "Ground - 2nd Floor",
        "description": "Chancellor, Vice Chancellor, Registrar, Accounts, Admissions, and Student Affairs offices."
    },
    "Academic Block - Ground Floor": {
        "x": 520, "y": 220, "category": "Academic", "floor": "Ground Floor",
        "description": "Dean's office, First-year lecture halls LH-01 to LH-08, and Student Helpdesk."
    },
    "Academic Block - 1st Floor (Computer Lab)": {
        "x": 520, "y": 190, "category": "Laboratories", "floor": "1st Floor",
        "description": "High-Performance Computing Lab, AI/ML Workstation Center, and CSE Faculty Cabins."
    },
    "Academic Block - 2nd Floor (Lecture Halls)": {
        "x": 520, "y": 160, "category": "Academic", "floor": "2nd Floor",
        "description": "Smart classrooms LH-201 to LH-212 equipped with interactive displays and IoT sensors."
    },
    "Academic Block - 3rd Floor (Faculty Cabins)": {
        "x": 520, "y": 130, "category": "Academic", "floor": "3rd Floor",
        "description": "Department of Computer Science & Engineering, HOD cabin, and research scholar workspace."
    },
    "Central Library - Ground Floor": {
        "x": 720, "y": 180, "category": "Library", "floor": "Ground Floor",
        "description": "Circulation desk, reference books, digital catalog terminal, and quiet reading zone."
    },
    "Central Library - 1st Floor (Reading Hall)": {
        "x": 720, "y": 150, "category": "Library", "floor": "1st Floor",
        "description": "E-Resource laboratory, IEEE/ACM journals section, and group discussion rooms."
    },
    "Seminar Hall & Auditorium": {
        "x": 640, "y": 320, "category": "Academic", "floor": "Ground Floor",
        "description": "Air-conditioned 600-seater auditorium for symposiums, guest lectures, and cultural events."
    },
    "Food Court / Cafeteria": {
        "x": 480, "y": 420, "category": "Dining", "floor": "Ground & 1st Floor",
        "description": "Multi-cuisine food court, bakery, Nescafe kiosk, and hygienic dining area."
    },
    "Student Activity Centre": {
        "x": 360, "y": 440, "category": "Facilities", "floor": "Ground Floor",
        "description": "Student clubs, indoor games, music studio, and robotics innovation hub."
    },
    "Hostel Block A (Boys Hostel)": {
        "x": 840, "y": 260, "category": "Hostels", "floor": "G + 4 Floors",
        "description": "Boys residential halls with Wi-Fi, dining mess, laundry facilities, and 24/7 warden."
    },
    "Hostel Block B (Girls Hostel)": {
        "x": 840, "y": 400, "category": "Hostels", "floor": "G + 4 Floors",
        "description": "Girls residential halls with biometric access control, infirmary, and study rooms."
    },
    "Sports Complex & Main Ground": {
        "x": 680, "y": 480, "category": "Facilities", "floor": "Ground",
        "description": "Football turf, cricket nets, tennis courts, athletic track, and campus gymnasium."
    },
    "Campus Health Centre": {
        "x": 320, "y": 380, "category": "Emergency", "floor": "Ground Floor",
        "description": "24/7 medical infirmary with duty doctors, registered nurses, oxygen, and ambulance dispatch."
    }
}

CAMPUS_EDGES = [
    ("Main Entrance & Security Gate", "Administrative Block", 120),
    ("Main Entrance & Security Gate", "Alliance University Car Parking", 140),
    ("Main Entrance & Security Gate", "Student Activity Centre", 160),
    ("Alliance University Car Parking", "Administrative Block", 130),
    ("Alliance University Car Parking", "Academic Block - Ground Floor", 190),
    ("Administrative Block", "Academic Block - Ground Floor", 110),
    ("Administrative Block", "Campus Health Centre", 75),
    ("Administrative Block", "Food Court / Cafeteria", 140),
    ("Campus Health Centre", "Food Court / Cafeteria", 85),
    ("Campus Health Centre", "Student Activity Centre", 90),
    ("Student Activity Centre", "Food Court / Cafeteria", 100),
    ("Academic Block - Ground Floor", "Academic Block - 1st Floor (Computer Lab)", 25),
    ("Academic Block - 1st Floor (Computer Lab)", "Academic Block - 2nd Floor (Lecture Halls)", 25),
    ("Academic Block - 2nd Floor (Lecture Halls)", "Academic Block - 3rd Floor (Faculty Cabins)", 25),
    ("Academic Block - Ground Floor", "Seminar Hall & Auditorium", 95),
    ("Academic Block - Ground Floor", "Central Library - Ground Floor", 130),
    ("Academic Block - Ground Floor", "Food Court / Cafeteria", 115),
    ("Central Library - Ground Floor", "Central Library - 1st Floor (Reading Hall)", 20),
    ("Central Library - Ground Floor", "Seminar Hall & Auditorium", 110),
    ("Central Library - Ground Floor", "Hostel Block A (Boys Hostel)", 140),
    ("Seminar Hall & Auditorium", "Food Court / Cafeteria", 90),
    ("Seminar Hall & Auditorium", "Sports Complex & Main Ground", 130),
    ("Food Court / Cafeteria", "Sports Complex & Main Ground", 150),
    ("Food Court / Cafeteria", "Hostel Block B (Girls Hostel)", 180),
    ("Hostel Block A (Boys Hostel)", "Hostel Block B (Girls Hostel)", 110),
    ("Hostel Block A (Boys Hostel)", "Sports Complex & Main Ground", 160),
    ("Hostel Block B (Girls Hostel)", "Sports Complex & Main Ground", 120)
]

ASSEMBLY_POINTS_MAPPING = {
    "Central Lawn in front of Academic Block": {
        "coords": (520, 270),
        "capacity": "1,500 people",
        "nearest_to": ["Academic Block", "Central Library", "Seminar Hall", "Administrative Block"]
    },
    "Open Ground near Sports Complex": {
        "coords": (680, 520),
        "capacity": "2,000 people",
        "nearest_to": ["Sports Complex", "Hostel Block A", "Hostel Block B", "Food Court"]
    },
    "Car Parking Area adjacent to Main Gate": {
        "coords": (180, 200),
        "capacity": "1,000 people",
        "nearest_to": ["Main Entrance", "Car Parking", "Administrative Block", "Campus Health Centre"]
    },
    "Basketball Court Area behind Hostel Block B": {
        "coords": (880, 440),
        "capacity": "800 people",
        "nearest_to": ["Hostel Block B", "Hostel Block A"]
    }
}

# ==============================================================================
# 3. AI CHATBOT EXTENSIVE KNOWLEDGE BASE
# ==============================================================================
AI_CAMPUS_KNOWLEDGE = [
    {
        "keywords": ["book", "library", "borrow", "reading", "study", "journal", "ieee"],
        "facility": "Central Library",
        "location": "Central Library Building, Ground & 1st Floor",
        "timings": "Mon - Sat: 8:00 AM - 10:00 PM | Exam Days: Open until 11:00 PM",
        "details": (
            "The Central Library houses over 75,000 reference books, international journals, "
            "and subscriptions to IEEE Xplore, ScienceDirect, and ACM Digital Library. "
            "Students can borrow up to 4 books for 14 days using their student RFID card."
        ),
        "contact": "Ext: 115 / library@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Central Library"
    },
    {
        "keywords": ["computer", "lab", "programming", "pc", "coding", "gpu", "machine learning"],
        "facility": "Computer Science Laboratories",
        "location": "Academic Block, 1st Floor (Labs 101 to 108)",
        "timings": "Mon - Fri: 8:30 AM - 7:00 PM",
        "details": (
            "Equipped with 250+ Intel Core i7 workstations, NVIDIA RTX GPUs for AI/ML projects, "
            "high-speed gigabit LAN, dual boot Linux/Windows, and licensed developer suites (MATLAB, Android Studio, VS Code)."
        ),
        "contact": "Ext: 122 / cselabs@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Academic Block - 1st Floor (Computer Lab)"
    },
    {
        "keywords": ["fee", "fees", "tuition", "account", "scholarship", "receipt", "finance", "payment"],
        "facility": "Accounts & Finance Office",
        "location": "Administrative Block, Ground Floor (Counter 3 & 4)",
        "timings": "Mon - Fri: 9:00 AM - 4:30 PM",
        "details": (
            "Handles tuition fee verification, exam fee receipts, scholarship disbursements, "
            "and education loan documentation. Online payments can also be completed via the Alliance Student Portal."
        ),
        "contact": "Ext: 104 / accounts@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Administrative Block"
    },
    {
        "keywords": ["food", "canteen", "cafeteria", "lunch", "breakfast", "dinner", "coffee", "mess", "nescafe"],
        "facility": "Food Court & Student Dining",
        "location": "Student Amenities Block (Ground & 1st Floor)",
        "timings": "Daily: 7:30 AM - 9:30 PM",
        "details": (
            "Offers multi-cuisine vegetarian and non-vegetarian meals, fresh juice counter, "
            "bakery, and a 24/7 Nescafe coffee kiosk. Weekly menu rotates and is monitored by the Student Mess Committee."
        ),
        "contact": "Ext: 130 / dining@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Food Court / Cafeteria"
    },
    {
        "keywords": ["medical", "health", "doctor", "medicine", "sick", "injury", "first aid", "hospital", "ambulance"],
        "facility": "Campus Health & Medical Centre",
        "location": "Ground Floor adjacent to Administrative Block",
        "timings": "24/7 Round-the-clock emergency medical service",
        "details": (
            "Resident medical officer, trained nursing staff, emergency observation beds, "
            "basic diagnostic equipment, and a dedicated on-campus ambulance on standby."
        ),
        "contact": "Emergency: +91 80 4619 9112 / Ext: 112",
        "action_link": "Campus Navigation -> Destination: Campus Health Centre"
    },
    {
        "keywords": ["hostel", "room", "accommodation", "curfew", "warden", "mess", "boys hostel", "girls hostel"],
        "facility": "Hostel Affairs & Student Housing",
        "location": "Hostel Block A & Block B Warden Offices",
        "timings": "Hostel Gates: Curfew is 9:00 PM for all residential students",
        "details": (
            "Separate boys and girls residential blocks with Wi-Fi, 24/7 security guard patrol, "
            "laundry services, solar hot water, and recreation rooms. Outstation leave requires digital warden permission."
        ),
        "contact": "Boys Warden: +91 80 4619 9201 | Girls Warden: +91 80 4619 9202",
        "action_link": "Campus Navigation -> Destination: Hostel Block A or B"
    },
    {
        "keywords": ["cse", "hod", "faculty", "professor", "department", "computer science", "dean"],
        "facility": "Department of Computer Science & Engineering",
        "location": "Academic Block, 3rd Floor",
        "timings": "Mon - Fri: 8:45 AM - 4:45 PM",
        "details": (
            "Houses the CSE HOD office, faculty consultation cabins, research scholar chambers, "
            "and department conference room. Students can schedule faculty meetings during office hours."
        ),
        "contact": "Ext: 120 / cse.office@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Academic Block - 3rd Floor"
    },
    {
        "keywords": ["wifi", "internet", "network", "login", "password", "it helpdesk", "portal"],
        "facility": "IT Infrastructure & Helpdesk",
        "location": "Administrative Block, Basement Floor",
        "timings": "Mon - Sat: 9:00 AM - 6:00 PM",
        "details": (
            "Campus-wide high-speed Wi-Fi network ('AU-Student-Secure'). Login using your University "
            "Registration ID and portal password. Contact IT Helpdesk for MAC address registration or portal issues."
        ),
        "contact": "Ext: 109 / ithelpdesk@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Administrative Block"
    },
    {
        "keywords": ["sports", "gym", "fitness", "football", "cricket", "basketball", "tennis", "ground"],
        "facility": "Sports Complex & Gymnasium",
        "location": "East Wing, behind Food Court",
        "timings": "Morning: 6:00 AM - 8:30 AM | Evening: 4:30 PM - 8:30 PM",
        "details": (
            "Modern air-conditioned gym with certified trainers, Olympic-sized outdoor basketball court, "
            "floodlit football field, synthetic badminton courts, and indoor table tennis arena."
        ),
        "contact": "Ext: 135 / sports@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Sports Complex & Main Ground"
    },
    {
        "keywords": ["exam", "results", "revaluation", "grade", "gpa", "timetable", "hall ticket"],
        "facility": "Office of Controller of Examinations (COE)",
        "location": "Administrative Block, 1st Floor",
        "timings": "Mon - Fri: 9:30 AM - 5:00 PM",
        "details": (
            "Coordinates mid-term and semester end examinations, hall ticket issuance, grade cards, "
            "transcripts, revaluation requests, and official certificate attestations."
        ),
        "contact": "Ext: 106 / coe@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Administrative Block"
    },
    {
        "keywords": ["placement", "internship", "job", "career", "interview", "recruitment", "resume"],
        "facility": "Career Advancement & Networking Office (CAN)",
        "location": "Student Activity Centre, 2nd Floor",
        "timings": "Mon - Fri: 9:00 AM - 5:30 PM",
        "details": (
            "Connects students with leading multinational corporations, organizes mock interviews, "
            "soft skill workshops, resume clinics, and on-campus recruitment drives."
        ),
        "contact": "Ext: 140 / placements@alliance.edu.in",
        "action_link": "Campus Navigation -> Destination: Student Activity Centre"
    }
]

# ==============================================================================
# 4. LITERATURE REVIEW PAPERS (FROM PROJECT PRESENTATION SLIDES)
# ==============================================================================
LITERATURE_REVIEW = [
    {
        "sno": 1,
        "author_year": "Fernandez et al., 2025 (Base Paper)",
        "title": "Smart Campus Directory: AI-Powered Navigation System Deployment",
        "methodology": "Uses A* pathfinding, SVG campus maps, QR-based PWA and AI virtual receptionist for campus navigation.",
        "findings": "100% route accuracy on validated campus layouts; AI assistant resolves 80% of queries.",
        "advantages": "Accurate navigation; AI assistance; emergency guidance; centralized administration.",
        "disadvantages": "Mainly focused on navigation; requires digital campus maps."
    },
    {
        "sno": 2,
        "author_year": "Wang et al., 2024",
        "title": "Campus Comprehensive Service App for College Students",
        "methodology": "Uses Flutter, Vue3 and microservices with integrated campus navigation and services.",
        "findings": "Provides navigation, notifications, emergency alerts and student services.",
        "advantages": "Unified campus services; scalable architecture.",
        "disadvantages": "Limited immersive/AR navigation."
    },
    {
        "sno": 3,
        "author_year": "Saradha et al., 2025",
        "title": "Smart AR Navigation: Enhancing Campus Wayfinding with Augmented Reality",
        "methodology": "Uses ARCore/ARKit, Unity3D, Blender and A*/Dijkstra for AR navigation.",
        "findings": "Provides shortest and alternative walking routes with AR guidance.",
        "advantages": "Interactive navigation; emergency routes; real-time information.",
        "disadvantages": "Mainly focuses on navigation."
    },
    {
        "sno": 4,
        "author_year": "Alsabbagh et al., 2020",
        "title": "University Campus Indoor Navigation for Android Devices using AR",
        "methodology": "Uses Unity, ARCore, Blender and A* over 3D floor plans.",
        "findings": "Provides AR guidance in GPS-denied indoor environments.",
        "advantages": "Indoor navigation; offline operation; obstacle-aware paths.",
        "disadvantages": "Requires 3D floor plans and markers."
    },
    {
        "sno": 5,
        "author_year": "Chotbenjamaporn et al., 2019",
        "title": "A Web-based Navigation System for a Smart Campus",
        "methodology": "Uses Google Maps API, Node.js and campus-specific route planning.",
        "findings": "Routes and indoor queries generated in under 3 seconds.",
        "advantages": "Multi-modal navigation; indoor floor plans; emergency alerts.",
        "disadvantages": "Web-based; indoor maps are mostly static."
    },
    {
        "sno": 6,
        "author_year": "Palarimath et al., 2025",
        "title": "Smart Campus, Smarter Students: AI-IoT Enabled Sustainable Spaces",
        "methodology": "Uses a 4-tier AI-IoT architecture for campus monitoring and management.",
        "findings": "18% improvement in space utilization and faster maintenance response.",
        "advantages": "Smart automation; resource management; real-time alerts.",
        "disadvantages": "Requires extensive sensor infrastructure."
    },
    {
        "sno": 7,
        "author_year": "Manassra & Işık, 2025",
        "title": "AI Supported Energy Management in Smart Campuses",
        "methodology": "Uses MLP, RNN, CNN and DQN with real-time sensor data.",
        "findings": "Achieved up to 59.125% energy reduction across lecture halls.",
        "advantages": "Intelligent energy management; reduced operational cost.",
        "disadvantages": "Mainly focused on energy management."
    },
    {
        "sno": 8,
        "author_year": "Sutjarittham et al., 2019",
        "title": "Experiences With IoT and AI in a Smart Campus for Optimizing Classrooms",
        "methodology": "Uses IoT occupancy sensors and ML models for attendance prediction and room allocation.",
        "findings": "Achieved over 10% facility cost savings; optimized classroom utilization.",
        "advantages": "Better classroom utilization; attendance prediction.",
        "disadvantages": "Focused mainly on classrooms."
    },
    {
        "sno": 9,
        "author_year": "Haggag et al., 2025",
        "title": "Integrating Advanced Technologies for Sustainable Smart Campus Development",
        "methodology": "Comprehensive survey of 122 studies covering AI, IoT, AR/VR, Digital Twins.",
        "findings": "Identifies major smart campus technologies and integration challenges.",
        "advantages": "Comprehensive smart-campus overview across multiple universities.",
        "disadvantages": "Survey only; no single implemented system."
    },
    {
        "sno": 10,
        "author_year": "Liu & Han, 2022",
        "title": "An IoT-based Smart Campus Monitoring System",
        "methodology": "Uses LoRa environmental sensors for air-quality and classroom monitoring.",
        "findings": "Provides real-time environmental monitoring and automated safety alerts.",
        "advantages": "Long-range monitoring; automatic alerts.",
        "disadvantages": "Small sample size; sensors can be intrusive."
    }
]

# ==============================================================================
# 5. INITIAL CAMPUS MAINTENANCE TICKETS
# ==============================================================================
SAMPLE_MAINTENANCE_TICKETS = [
    {
        "id": "AU-REQ-2026-081",
        "title": "Overhead Projector Display Flickering in LH-204",
        "category": "IT / Equipment",
        "location": "Academic Block - 2nd Floor (Lecture Halls)",
        "reported_by": "Vidhyasri. R (2411021060047)",
        "priority": "High",
        "status": "In Progress",
        "description": "HDMI port connection loose and lamp flickering during afternoon lectures.",
        "created_at": "2026-11-04 11:20:00",
        "assigned_to": "IT Support Desk #3"
    },
    {
        "id": "AU-REQ-2026-082",
        "title": "Water Cooler Filter Replacement Required",
        "category": "Plumbing",
        "location": "Central Library - Ground Floor",
        "reported_by": "Bhavishya Raj M.H (2411021060805)",
        "priority": "Medium",
        "status": "Resolved",
        "description": "Drinking water cooler indicator showing red replace-filter light near circulation desk.",
        "created_at": "2026-11-03 14:15:00",
        "assigned_to": "Campus Maintenance Team"
    },
    {
        "id": "AU-REQ-2026-083",
        "title": "Air Conditioning Temperature Sensor Error in Lab 102",
        "category": "Electrical",
        "location": "Academic Block - 1st Floor (Computer Lab)",
        "reported_by": "Samriddhi Singh (2411021060838)",
        "priority": "High",
        "status": "Pending Inspection",
        "description": "AC unit tripping circuit breaker under high computing load.",
        "created_at": "2026-11-05 09:40:00",
        "assigned_to": "Electrical Maintenance Division"
    }
]

