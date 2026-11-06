# 🛠️ Comprehensive Developer Technical Documentation
## Smart Campus Management System Using AI
**Alliance University • Department of Computer Science & Engineering**  
**Course Code:** E1CSA313 Design Project - 1  
**Faculty Mentor:** Dr. Vinita Nair  
**Academic Year:** 2026-2027  
**Version:** 2.4.0 (Enterprise Gold)

---

## 👥 Student Authors & Roles
1. **BHAVISHYA RAJ M.H** – `2411021060805` *(Team Lead & Full-Stack Developer)*
2. **VIDHYASRI. R** – `2411021060047` *(AI/ML & Database Specialist)*
3. **SAMRIDDHI SINGH** – `2411021060838` *(System Architecture & Navigation Engineer)*
4. **R. DHARSHINI** – `2411021060087` *(Emergency Systems & UI/UX Developer)*

---

## 1. System Overview & Module Integration

The **Smart Campus Management System Using AI** is a unified multi-tier campus operating platform. It eliminates traditional information fragmentation across university departments by consolidating:
1. **Student Executive Front Page:** Identity card, attendance, schedule, and quick launchpad.
2. **Module 1 (Campus Navigation):** Graph-based wayfinding using A* (A-Star) with Euclidean distance heuristic and Dijkstra shortest-path algorithms across 16 campus locations.
3. **Module 2 (AI-Based Campus Management):** Natural language virtual assistant, classroom/lab occupancy predictive modeling, and maintenance auto-triage.
4. **Module 3 (Centralized Campus & Emergency Services):** Emergency SOS dispatcher, incident auditing, real-time screen alert modal (`st.dialog`), notifications management, circulars publisher, and 24/7 helplines.
5. **Module 4 (Campus Issue Reporting):** Full maintenance ticket lifecycle management with status progression.
6. **Module 5 (Project Research Deck):** In-app presentation viewer containing the 10-paper literature review, methodology, and experimental results.

---

## 2. Architecture & Data Flow

```
+-----------------------------------------------------------------------------------+
|                                 PRESENTATION LAYER                                |
|                              Streamlit Frontend (app.py)                          |
|                                                                                   |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|  | Student Front Page |  | A* Navigation Map  |  | AI Campus Virtual Assistant |  |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|  | Emergency SOS Hub  |  | Maintenance Triage |  | Presentation Slide Viewer   |  |
|  +--------------------+  +--------------------+  +-----------------------------+  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                 BUSINESS LOGIC LAYER                              |
|                                                                                   |
|  - CampusNavigator (modules/navigation.py): A* & Dijkstra pathfinding             |
|  - CampusAI (modules/chatbot.py): NLP query engine & room occupancy model         |
|  - EmergencySystem (modules/emergency.py): SOS dispatching & evacuation routing   |
|  - NotificationManager (notifications_manager.py): Inbox filtering & CRUD         |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                  DATA ACCESS LAYER                                |
|                                                                                   |
|         +-------------------------------+-------------------------------+         |
|         |                               |                               |         |
|         v                               v                               v         |
|  [SupabaseManager]            [Local JSON Fallback]             [Seed Data]       |
| (supabase_client.py)         (campus_local_db.json)         (data/seed_data.py)   |
|         |                               |                               |         |
|         v                               v                               v         |
|  PostgreSQL Cloud              Disk File Storage              In-Memory POI Graph |
+-----------------------------------------------------------------------------------+
```

---

## 3. Key Source Files & Functions

| File | Purpose | Key Classes & Functions |
|---|---|---|
| `app.py` | Main application controller and Streamlit UI. | `show_emergency_dialog()`, multi-page routing, student switcher. |
| `config.py` | University configuration, helplines, locations, and environment loading. | `DEFAULT_SUPABASE_URL`, `CAMPUS_LOCATIONS`, `EMERGENCY_CONTACTS`. |
| `modules/navigation.py` | Pathfinding and map generation. | `CampusNavigator.find_route()`, `render_dynamic_map()`, `find_nearest_assembly_point()`. |
| `modules/chatbot.py` | NLP campus assistant and predictive models. | `CampusAI.answer_query()`, `predict_room_occupancy()`, `triage_maintenance_issue()`. |
| `modules/emergency.py` | Emergency orchestration and evacuation guidance. | `EmergencySystem.dispatch_sos()`, `submit_detailed_report()`. |
| `notifications_manager.py` | Notification metrics, filters, and alert logic. | `NotificationManager.get_stats()`, `filter_notifications()`. |
| `supabase_client.py` | Supabase Cloud PostgREST client with local JSON fallback. | `SupabaseManager.add_notification()`, `fetch_emergency_reports()`. |
| `data/seed_data.py` | Campus nodes, edges, student profiles, and literature review. | `STUDENT_TEAM`, `CAMPUS_NODES`, `LITERATURE_REVIEW`. |
| `database/queries.py` | SQL schema definitions and maintenance ticket storage. | `load_maintenance_tickets()`, `save_maintenance_ticket()`. |
| `utils/helpers.py` | Base64 encoders and Web Audio synthesizer sirens. | `get_image_base64()`, `generate_audio_siren_html()`. |

---

## 4. Verification & Testing

All modules have been verified for syntax, runtime execution, and data integrity:
- **Python Syntax Compilation:** Verified with `py_compile` across all files.
- **Pathfinding Precision:** Tested on 16 campus nodes; Euclidean A* and Dijkstra paths validated.
- **NLP Query Accuracy:** Tested against campus queries with confidence metric resolution.
- **Database Resilience:** Tested with Supabase online mode and transparent local offline JSON fallback.
