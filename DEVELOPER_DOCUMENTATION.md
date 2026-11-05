# 🛠️ Developer Technical Documentation
## Smart Campus Management System — Emergency & Notification Management
**Alliance University • Department of Computer Science & Engineering**  
**Course Code:** E1CSA313 Design Project - 1  
**Project Mentor:** Dr. Vinita Nair  
**Module Focus:** Centralized Campus & Emergency Services (Emergency & Notification Subsystem)

---

## 1. System Overview & Objective

The **Emergency & Notification Management Subsystem** is an enterprise-grade campus safety and communications engine designed for the **Alliance University Smart Campus Management System**.

The module solves critical limitations observed in traditional university infrastructure:
1. Fragmented communication channels between administration, security, and students.
2. Delayed distress response during medical, fire, or safety emergencies.
3. Lack of unified online records for campus circulars and incident audits.

### Core Deliverables Implemented:
1. **Emergency SOS Trigger:** Rapid one-click distress signal dispatcher for students.
2. **Formal Incident Reporting:** Multi-category emergency reporting interface with severity classification.
3. **Cloud Database Persistence:** PostgreSQL cloud database integration via **Supabase** with automatic local JSON fallback.
4. **Real-time Screen Alert Modal:** Active emergency dialog (`st.dialog`) with audible synthesizer alert and safe assembly guidance.
5. **Student Notification Management Center:** Comprehensive notification inbox featuring search, category filtering, unread status indicators, and batch actions.

---

## 2. Architectural Blueprint

```
+-----------------------------------------------------------------------------------+
|                                 PRESENTATION LAYER                                |
|                                (Streamlit App: app.py)                            |
|                                                                                   |
|  +---------------------+   +---------------------+   +-------------------------+  |
|  |   Emergency SOS     |   | Incident Reporting  |   |   Notification Center   |  |
|  |   (Pulsing Action)  |   | (Multi-field Form)  |   | (Filter / Search / CRUD)|  |
|  +----------+----------+   +----------+----------+   +------------+------------+  |
|             |                         |                           |               |
|             +-------------------------+---------------------------+               |
|                                       |                                           |
|                                       v                                           |
|                     +-----------------------------------+                         |
|                     | Emergency Popup Alert (st.dialog) |                         |
|                     |      + HTML5 Audio Synthesizer    |                         |
|                     +-----------------+-----------------+                         |
+---------------------------------------|-------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                              BUSINESS LOGIC LAYER                                 |
|                        (notifications_manager.py)                                 |
|                                                                                   |
|   - NotificationManager.trigger_sos()                                             |
|   - NotificationManager.report_incident()                                         |
|   - NotificationManager.filter_notifications()                                    |
|   - NotificationManager.get_stats()                                               |
+---------------------------------------+-------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                               DATA ACCESS LAYER                                   |
|                             (supabase_client.py)                                  |
|                                                                                   |
|            +--------------------------+---------------------------+               |
|            |                          |                           |               |
|            v                          v                           v               |
|   [PostgREST REST API]      [Local JSON Fallback]       [Session State]           |
|  (HTTPS / Authorization)   (campus_local_db.json)    (st.session_state)          |
+------------+--------------------------+---------------------------+---------------+
             |                          |
             v                          v
+------------------------+   +----------------------+
|    SUPABASE CLOUD      |   |  LOCAL WORKSPACE     |
| (PostgreSQL Database)  |   | (campus_local_db.json|
| - campus_notifications |   +----------------------+
| - emergency_reports    |
+------------------------+
```

---

## 3. Detailed File & Component Breakdown

### 3.1 `app.py` — Presentation & Controller Entrypoint
- **Role:** Main UI execution script rendering the dark-themed Alliance University web interface.
- **Styling Architecture:**
  - CSS injection via `st.markdown("<style>...</style>", unsafe_allow_html=True)`.
  - Palette: Dark charcoal background (`#0d1117`), dark slate cards (`#161b22`), border stroke (`#30363d`), Alliance crimson accent (`#8b0000` / `#b91c1c`), high-visibility red (`#ef4444`).
  - Brand identity: Alliance University circular crest logo encoded into Base64 for zero-latency local asset embedding.
- **Session State Variables (`st.session_state`):**
  - `supabase_url`: Supabase endpoint string.
  - `supabase_key`: Supabase API key string.
  - `dismissed_alerts`: Set of string UUIDs representing emergency alerts acknowledged by the active user.
  - `popup_triggered`: Boolean flag controlling immediate execution of `show_emergency_dialog()`.
  - `current_alert_details`: Dictionary containing active emergency payload.
  - `sound_enabled`: Boolean flag toggling Web Audio synthesizer playback.
- **Dialog Architecture (`@st.dialog`):**
  - Decorator: `@st.dialog("🚨 CAMPUS EMERGENCY ALERT - IMMEDIATE ACTION REQUIRED", width="large")`.
  - Trigger condition: Evaluated at top of script run whenever `db.get_active_emergency()` returns an unresolved emergency whose ID is absent from `dismissed_alerts`.

---

### 3.2 `supabase_client.py` — Data Access & Resiliency Layer
- **Role:** Abstraction layer managing communication with Supabase PostgreSQL cloud database, featuring seamless fallback to a local JSON database file.
- **Class: `SupabaseManager`:**
  - `__init__(supabase_url, supabase_key)`: Cleans URL, validates format, sets `is_configured` boolean.
  - `get_headers()`: Returns HTTP headers required by Supabase PostgREST:
    ```python
    {
        "apikey": self.key,
        "Authorization": f"Bearer {self.key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    ```
  - `test_connection() -> (bool, str)`: Issues `GET /rest/v1/campus_notifications?select=id&limit=1` with 5s timeout to test authentication and reachability.
  - `fetch_notifications() -> List[Dict]`: Retrieves notices ordered by `created_at.desc`.
  - `add_notification(...) -> Dict`: Creates notice; syncs to Supabase PostgREST or local store.
  - `mark_notification_as_read(id, is_read=True) -> bool`: Executes `PATCH /rest/v1/campus_notifications?id=eq.{id}`.
  - `mark_all_notifications_as_read() -> bool`: Batch-updates all unread rows.
  - `delete_notification(id) -> bool`: Executes `DELETE /rest/v1/campus_notifications?id=eq.{id}`.
  - `add_emergency_report(...) -> Dict`: Saves full incident report to `emergency_reports` table AND creates a mirrored critical alert in `campus_notifications`.
  - `get_active_emergency() -> Optional[Dict]`: Scans active records for unhandled life-safety hazards.
  - `resolve_emergency(id) -> bool`: Marks incident and mirrored notifications as `resolved`.
- **Local Fallback Mechanics (`_ensure_local_db`, `_save_local_db`):**
  - When Supabase credentials are not provided or network is offline, all reads and writes execute against `campus_local_db.json`.
  - Guarantees the application **never crashes** due to network timeouts or missing cloud configuration.

---

### 3.3 `notifications_manager.py` — Business Logic Engine
- **Role:** Intermediate controller implementing search filters, aggregations, distress routines, and browser audio triggers.
- **Class: `NotificationManager`:**
  - `get_stats() -> Dict[str, int]`: Returns real-time counts (`total`, `unread`, `emergencies`).
  - `filter_notifications(category, status_filter, search_query) -> List[Dict]`: Multi-predicate in-memory filter matching title, message, sender, and location against search tokens.
  - `trigger_sos(...) -> Dict`: High-level wrapper executing immediate SOS dispatch with default "Critical" life-safety priority.
  - `report_incident(...) -> Dict`: Form validator and dispatcher for structured user incident reports.
- **Audio Synthesizer (`render_audio_siren`):**
  - Injects Web Audio API JavaScript into the DOM.
  - Generates a custom 800Hz-to-400Hz sawtooth frequency sweep simulating an emergency alarm tone directly through the student's browser speakers without external MP3 audio file dependencies.

---

### 3.4 `config.py` — University Constants & Environment Resolution
- **Role:** Centralized configuration repository for POIs, helplines, metadata, and `.env` parsing.
- **Built-in Environment Reader (`_load_env_file`):**
  - First attempts `python-dotenv`.
  - Falls back to native ASCII file parsing if third-party modules are unavailable.
- **Constants:**
  - `UNIVERSITY_NAME`: `"Alliance University"`
  - `ACCREDITATION`: `"NAAC Grade A+ Accredited University"`
  - `EMERGENCY_CONTACTS`: Comprehensive directory of campus security, medical centre, women's helpline, and national emergency lines.
  - `CAMPUS_LOCATIONS`: Canonical list of 15 Alliance University campus locations for dropdown validation.
  - `EMERGENCY_TYPES`: Pre-classified emergency taxonomies (Medical, Fire, Threat, Ragging, etc.).
  - `ASSEMBLY_POINTS`: Pre-defined safe evacuation meeting zones across campus.

---

### 3.5 `schema.sql` — PostgreSQL Database Schema
Defines the relational architecture and Row Level Security (RLS) policies executed within the Supabase SQL Engine:

```sql
-- 1. Notifications Table
CREATE TABLE IF NOT EXISTS public.campus_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'announcement', -- 'emergency', 'announcement', 'security', 'medical'
    priority TEXT NOT NULL DEFAULT 'medium',        -- 'critical', 'high', 'medium', 'low'
    sender TEXT NOT NULL DEFAULT 'Campus Administration',
    location TEXT DEFAULT 'Campus-wide',
    is_emergency BOOLEAN DEFAULT FALSE,
    is_read BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'active',                   -- 'active', 'resolved', 'archived'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Emergency Reports Table
CREATE TABLE IF NOT EXISTS public.emergency_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    emergency_type TEXT NOT NULL,
    location TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'Critical',     -- 'Critical', 'High', 'Medium'
    description TEXT,
    status TEXT DEFAULT 'Active',                  -- 'Active', 'Dispatched', 'Resolved'
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Row Level Security (RLS) Configuration:
To ensure open access for prototype demonstration without requiring authentication tokens:
- Tables enable RLS: `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`
- Policies grant public `SELECT`, `INSERT`, `UPDATE`, and `DELETE` access to `anon` and `authenticated` roles.

---

## 4. Workflows & Sequence Flows

### Workflow 1: Instant Emergency SOS Activation
```
[Student in Danger]
        │
        ▼ (Clicks "🚨 TRIGGER EMERGENCY SOS NOW")
[app.py: Tab 1]
        │
        ▼ Calls manager.trigger_sos()
[notifications_manager.py]
        │
        ▼ Calls db.add_emergency_report()
[supabase_client.py]
        ├─► [Supabase Cloud: POST /rest/v1/emergency_reports]
        └─► [Supabase Cloud: POST /rest/v1/campus_notifications (is_emergency=True)]
        │
        ▼ Updates st.session_state.current_alert_details
[app.py: Trigger Rerun]
        ├─► render_audio_siren() (Browser Siren Sounds)
        ├─► show_emergency_dialog() (Popup Modal Appears on Screen)
        └─► Persistent Red Alert Banner rendered at top of all pages
```

---

### Workflow 2: Student Incident Report Submission
```
[Student fills Incident Form]
        │
        ▼ (Name, ID, Phone, Category, Specific Landmark, Severity, Description)
[app.py: Form Submit]
        │
        ▼ Calls manager.report_incident()
[notifications_manager.py]
        │
        ▼ Calls db.add_emergency_report()
[supabase_client.py]
        ├─► Inserts row into public.emergency_reports
        ├─► If severity == 'Critical', creates broadcast notification
        └─► Returns created record payload
        │
        ▼ (UI updates with success toast, balloon animation & live table update)
```

---

### Workflow 3: Notification Management & Read Status Lifecycle
```
[Student views Notification Center]
        │
        ▼ Queries manager.filter_notifications(category, status, search)
[In-Memory Filter Engine]
        │
        ▼ Renders interactive dark notification cards
[Card User Action]
        ├─► "Mark Read"   ──► db.mark_notification_as_read(id, True)  ──► Updates DB & State
        ├─► "Mark Unread" ──► db.mark_notification_as_read(id, False) ──► Updates DB & State
        ├─► "Delete"      ──► db.delete_notification(id)             ──► Removes from DB & State
        └─► "Mark All"    ──► db.mark_all_notifications_as_read()     ──► Batch updates all unread
```

---

## 5. Security & Privacy Safeguards

1. **Zero Credential Exposure:**
   - `.env` contains the Supabase private Anon key and URL.
   - [`.gitignore`](file:///c:/Users/ramas/OneDrive/Desktop/smart_campus_management_system/.gitignore) explicitly ignores `.env` and local cache files.
   - [`.env.example`](file:///c:/Users/ramas/OneDrive/Desktop/smart_campus_management_system/.env.example) is committed to Git with sanitized placeholder values.
2. **Offline Decoupling:**
   - No external CDN dependencies for logos or map graphics; all assets are loaded locally from `alliance_logo.png`, `campus_navigation_map.png`, and `navigation_icon.png`.
3. **Safe Fallback Execution:**
   - Network failure or API rate limiting automatically shifts the database engine to internal JSON operations without raising fatal Python exceptions.

---

## 6. How to Run & Verify

### Environment Setup:
```powershell
# Navigate to workspace
cd "c:\Users\ramas\OneDrive\Desktop\smart_campus_management_system"

# Launch Streamlit server
streamlit run app.py
```

### Access URL:
- Local Web Interface: `http://localhost:8501`

### Running Headless Verification Tests:
```powershell
python -m py_compile app.py config.py supabase_client.py notifications_manager.py
```

---

## 7. Future Extension Roadmap
1. **Supabase Realtime WebSockets:** Implement `supabase.channel()` to push instant alerts without manual page refresh.
2. **SMS/WhatsApp Gateway:** Connect Twilio or AWS SNS to trigger physical phone calls and SMS dispatches to campus security guards upon SOS press.
3. **PWA Mobile Packaging:** Package with progressive web app manifests for home-screen installation on Android/iOS devices.
4. **IoT Sensor Feeds:** Integrate campus smoke detector and CCTV tripwire webhooks into `add_emergency_report()`.

---
*Documentation compiled for Alliance University E1CSA313 Design Project - 1 evaluation.*
