# 🏫 Smart Campus Management System Using AI
## Alliance University • E1CSA313 Design Project - 1
**Faculty Mentor:** Dr. Vinita Nair  
**Accreditation:** NAAC Grade A+ Accredited University  
**Academic Year:** 2026-2027

---

## 👥 Student Research & Development Team
| Student Name | Registration ID | Project Role | Department |
|---|---|---|---|
| **BHAVISHYA RAJ M.H** | `2411021060805` | Team Lead & Full-Stack Developer | Computer Science & Engineering |
| **VIDHYASRI. R** | `2411021060047` | AI/ML & Database Specialist | Computer Science & Engineering |
| **SAMRIDDHI SINGH** | `2411021060838` | System Architecture & Navigation Engineer | Computer Science & Engineering |
| **R. DHARSHINI** | `2411021060087` | Emergency Systems & UI/UX Developer | Computer Science & Engineering |

---

## 🌟 Complete Project Features & Modules

### 1. 🎓 Beautiful Student Front Page & University Portal
- **Alliance University Crest & NAAC Grade A+ Badge:** Official university branding with dark-charcoal and crimson theme.
- **Digital Student Identity Card:** Interactive student card featuring student avatar, registration ID, semester, attendance rate (96.4%), CGPA (9.24), enrolled credits, and RFID access status.
- **Active Student Switcher:** Switch seamlessly between team members (**Bhavishya Raj M.H**, **Vidhyasri. R**, **Samriddhi Singh**, **R. Dharshini**) in the sidebar.
- **Quick Launchpad:** Direct 1-click access to Navigation, AI Assistant, Emergency SOS, Announcements, Maintenance, and Project Presentation Deck.
- **Today's Academic Schedule & Live Campus Circulars Feed:** Timetable for 5th Semester CSE classes and live administrative notices.

### 2. 📍 Module 1: Campus Navigation Module
- **A* & Dijkstra Pathfinding Algorithms:** Dynamic shortest-path calculation across 16 university buildings, laboratories, lecture halls, and facilities.
- **Live Metrics:** Real-time walking distance (metres), estimated walking time (minutes), and waypoint count.
- **Turn-by-Turn Navigation:** Sequential floor-level walking directions.
- **Interactive Route Map Visualizer:** Dynamically drawn canvas rendering walking paths, building footprints, start pin (A), and destination flag (B).
- **Emergency Evacuation Navigator:** 1-click calculator for the nearest Safe Assembly Point (Central Lawn, Sports Ground, Parking) from any campus location.

### 3. 🤖 Module 2: AI-Based Campus Management Module
- **Intelligent Virtual Assistant (Chat):** Natural Language Processing with semantic keyword matching covering library hours, computer labs, fee enquiries, cafeteria menus, CSE HOD, Wi-Fi helpdesk, hostel policies, and exam schedules.
- **Classroom & Lab Occupancy Predictor:** AI space utilization model predicting seat availability and class occupancy by room, day of week, and time slot.
- **Maintenance Query Auto-Triage:** Automatically categorizes maintenance complaints, determines severity, and assigns the appropriate campus division.

### 4. 🛡️ Module 3: Centralized Campus & Emergency Services
- **Emergency SOS System:** Rapid distress signal button with audible synthesizer siren, broadcast to security, and instant modal popup alert.
- **Incident Reporting:** Multi-field emergency report form with severity classification and Supabase Cloud storage.
- **Real-Time Screen Popup Alert (`@st.dialog`):** High-priority alert dialog appearing on student screens during active emergencies.
- **Student Notification Management Center:** Filter by category, unread status, search by keyword, mark as read, and batch actions.
- **Campus Announcements Publisher:** Circular publishing form with live feed matching presentation screenshots.
- **Emergency Directory & Assembly Points:** 24/7 security, health center, women's safety, and national emergency contacts.
- **Supabase Cloud Database Integration:** PostgreSQL cloud persistence with transparent local JSON offline fallback.

### 5. ⚠️ Campus Issue Reporting & Maintenance Tracker
- **Maintenance Ticket Submission:** Report electrical, plumbing, IT, or facility defects.
- **Live Ticket Tracker:** Real-time status tracking (Submitted, In Progress, Resolved) with assigned technical divisions.

### 6. 📊 Project Presentation Deck & Research Documentation
- **In-App Slide Viewer:** Comprehensive slide deck covering:
  - Project Agenda
  - Introduction, Challenge & Problem Statement
  - Complete **10-Paper Literature Review Table** (Fernandez, Wang, Saradha, Alsabbagh, Chotbenjamaporn, Palarimath, Manassra, Sutjarittham, Haggag, Liu)
  - Observations & Limitations from Literature
  - System Architecture & Workflow Diagram
  - Hardware & Software Specifications
  - Results & Discussion
  - Conclusion & Academic References

---

## 🚀 How to Run the Project

### Step 1: Open Terminal in Project Folder
Ensure you are in the project folder:
```bash
cd c:\Users\ramas\OneDrive\Desktop\revised_cmsuai
```

### Step 2: Launch Streamlit
```bash
streamlit run app.py
```

### Step 3: View in Browser
Open:
```
http://localhost:8501
```

---

## ☁️ Supabase Cloud Configuration (Optional)
The system works out-of-the-box with local offline JSON fallback (`campus_local_db.json`). To connect your live Supabase database:
1. Open the app -> Go to **"Campus & Emergency Services"** -> Tab **"☁️ 6. Supabase Cloud Setup"**.
2. Enter your `SUPABASE_URL` and `SUPABASE_KEY`.
3. Click **"Save & Test Supabase Credentials"**.
4. The sidebar will indicate **🟢 Supabase Connected**.

---

## 🏛️ Project Information
- **Institution:** Alliance University, Bengaluru
- **Course:** E1CSA313 Design Project - 1
- **Faculty Mentor:** Dr. Vinita Nair
- **Version:** 2.4.0 (Enterprise Gold)
