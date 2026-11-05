# 🏫 Smart Campus Management System Using AI
## Alliance University • E1CSA313 Design Project - 1
**Mentor:** Dr. Vinita Nair  
**Your Module:** Emergency & Notification Management (Centralized Campus & Emergency Services)

---

## 🎯 The 5 Things Built For You

You were assigned 5 core features in your design project. All 5 are completely built and integrated into the exact dark-themed Alliance University design shown in your presentation:

| # | Feature | Where to Find It in the App | What It Does |
|---|---|---|---|
| **1** | **Emergency SOS Button for Students** | **Tab 1: 🚨 1. Emergency SOS** | Big pulsing red button for students in danger. Auto-detects/selects location, selects emergency type, saves incident to Supabase, and triggers emergency siren & screen alert! |
| **2** | **A Way to Report an Emergency** | **Tab 2: 📝 2. Report Emergency** | A complete incident reporting form (student name, ID, phone, emergency type, campus landmark, severity level, description). Saves instantly to Supabase cloud! |
| **3** | **Saving Notifications Online (Supabase)** | **Tab 6: ☁️ 6. Supabase Cloud Setup** | Integrated with Supabase PostgreSQL cloud database. Saves all announcements, reports, and SOS records in real-time. Also includes automatic local fallback so it never crashes! |
| **4** | **Emergency Screen Popup Alert** | **Anywhere in the App (Automatic Modal)** | When an SOS or critical emergency occurs, a high-impact popup alert modal (`st.dialog`) appears on screen with flashing red warnings, evacuation steps, and audio alarm sound! |
| **5** | **Student Notification Management Page** | **Tab 3: 🔔 3. Manage Notifications** | A full notification dashboard where students can filter by category, search by keyword, view unread badges, mark as read, and delete notifications. |

---

## 🚀 Quick Start Guide (Run It Right Now in 1 Minute!)

### Step 1: Open Terminal in VS Code
Open your project folder `smart_campus_management_system` in VS Code.  
Press `` Ctrl + ` `` to open the terminal.

### Step 2: Start the Application
Run this single command:
```bash
streamlit run app.py
```

Your web browser will automatically open:
```
http://localhost:8501
```

> **Note:** The app works **immediately out-of-the-box** using built-in local database storage with the sample announcements from your PPT ("Seminar Announcement" and "Library Timings Update"). You can test all 5 features right away!

---

## ☁️ How to Connect Supabase (Free Cloud Database)

To save your notifications and emergencies online to **Supabase** as required by your project, follow these very simple steps:

### Step 1: Create a Free Supabase Account
1. Open your browser and go to: **[https://supabase.com](https://supabase.com)**
2. Click **"Start your project"** (it is 100% free).
3. Sign in with GitHub or your Google email.

### Step 2: Create a New Project
1. Click the green button **"New project"**.
2. Fill in:
   - **Name:** `Smart Campus`
   - **Database Password:** Enter any password you will remember (e.g., `AllianceCampus2026!`).
   - **Region:** Choose closest (e.g. `Singapore` or `India/Mumbai`).
3. Click **"Create new project"** (takes about 1-2 minutes to initialize).

### Step 3: Run the Database Tables (1-Click Copy-Paste)
1. On the left sidebar in your Supabase dashboard, click the **"SQL Editor"** icon (looks like `>_`).
2. Click **"+ New query"**.
3. Open the file **`schema.sql`** in this project folder, select all text (`Ctrl + A`), and copy it (`Ctrl + C`).
4. Paste it into the Supabase SQL editor.
5. Click the green **"Run"** button in the bottom right!  
   *(You will see `Success. No rows returned` — both `campus_notifications` and `emergency_reports` tables are now created in the cloud!)*

### Step 4: Get Your API Keys
1. In your Supabase dashboard, click the **Settings** (gear icon ⚙️) at the bottom left.
2. Under "Configuration", click **"Data API"** (or **"API"**).
3. Copy these two values:
   - **Project URL** (looks like `https://abcdefghijkl.supabase.co`)
   - **Project API keys -> `anon` / `public`** (a long string starting with `eyJ...`)

### Step 5: Connect it in the App
You can connect in either of two easy ways:
- **Way A (Inside the Web App):** Open the app -> Go to **"Campus & Emergency Services"** -> Click **"☁️ 6. Supabase Cloud Setup"** -> Paste your URL and Anon Key -> Click **"Save & Test Supabase Credentials"**.
- **Way B (In `.env` file):** Rename `.env.example` to `.env` and paste your keys:
  ```env
  SUPABASE_URL=https://your-project-id.supabase.co
  SUPABASE_KEY=your-anon-key-here
  ```

Once connected, the sidebar badge turns **🟢 Supabase Connected**!

---

## 🎬 How to Demonstrate Each Feature to Your Mentor (Dr. Vinita Nair)

### Demo 1: Emergency SOS Button (Feature 1)
1. In the sidebar, select **"Campus & Emergency Services"**.
2. Click on the first tab: **"🚨 1. Emergency SOS"**.
3. Point out the student details (Name, ID, Contact) and the location selector (`Academic Block - 1st Floor`).
4. Click the large red button: **"🚨 TRIGGER EMERGENCY SOS NOW"**.
5. **Notice what happens:**
   - The emergency siren sounds.
   - A critical emergency is recorded.
   - The on-screen emergency modal popup opens immediately!

### Demo 2: Emergency Screen Popup Alert (Feature 4)
1. When the SOS is triggered, a large modal alert appears over the screen:
   - Title: `🚨 CAMPUS EMERGENCY ALERT - IMMEDIATE ACTION REQUIRED`
   - Location: `Academic Block - 1st Floor`
   - Safe Evacuation Instructions (Central Lawn assembly area, avoid elevators).
   - Direct helpline numbers.
2. Click **"✅ I Am Safe / Acknowledge Alert"** to close the popup.
3. Notice that the top banner stays active in red until security marks it resolved!
4. Show the sidebar button: **"👁️ Re-open Emergency Popup"** or **"✅ Resolve / Clear Emergency"**.

### Demo 3: Emergency Incident Reporting (Feature 2)
1. Click the second tab: **"📝 2. Report Emergency"**.
2. Fill in the form:
   - Name: `Vidhyasri R.`
   - Student ID: `2411021060047`
   - Category: `🔥 Fire Hazard / Smoke Alert`
   - Location: `Central Library`
   - Severity: `High`
   - Description: `Smoke detected in server room behind reading hall.`
3. Click **"📤 Submit Emergency Report to Supabase"**.
4. Show the balloons and the **"📋 Recent Emergency Incident Log (Supabase Feed)"** table showing the live record!

### Demo 4: Student Notification Center & Management (Feature 5)
1. Click the third tab: **"🔔 3. Manage Notifications"**.
2. Show the 4 summary metric boxes:
   - Total Notifications
   - Unread Notices
   - Active Emergencies
   - Read & Handled
3. Show the filter buttons:
   - Click category filter: **"🚨 Emergencies"** (shows only emergency notices).
   - Click status filter: **"Unread Only"**.
   - Type in search box: `Seminar` or `Fire`.
4. Click **"Mark Read"** on any notification card — the badge turns from `🔴 Unread` to `✅ Read`.
5. Click **"✅ Mark All as Read"** to update all at once!

### Demo 5: Online Storage in Supabase (Feature 3)
1. Open your Supabase Dashboard in another browser tab.
2. Click **"Table Editor"** -> select **`campus_notifications`** or **`emergency_reports`**.
3. Show Dr. Vinita Nair the rows updating live with timestamps, student IDs, and locations!

---

## 📁 File Structure

```
smart_campus_management_system/
│
├── app.py                      # Main Streamlit web application with full Alliance UI & navigation
├── config.py                   # Alliance University constants, emergency helplines & locations
├── supabase_client.py          # Supabase cloud REST client with automatic local JSON fallback
├── notifications_manager.py    # SOS triggers, incident reporting, sound alerts, and filtering
├── schema.sql                  # 1-click database schema for Supabase SQL Editor
├── requirements.txt            # Python dependencies (streamlit, requests, python-dotenv)
├── .env.example                # Template for Supabase credentials
├── .streamlit/
│   ├── config.toml             # Dark theme and server configuration matching PPT slides
│   └── credentials.toml        # Headless local settings
└── README.md                   # This step-by-step guide
```

---

## 🎨 Matching Your Team's PPT Slides
The app has been styled to exactly match your team's presentation:
- **Alliance University Crest & NAAC A+ Badge** at the top.
- **Dark Theme:** Deep charcoal `#0d1117` background with crimson/maroon `#b91c1c` accents.
- **All 5 Pages from the PPT are included in the sidebar:**
  - `Home`: Project summary, team members & mentor name.
  - `Campus Navigation`: 663 mapped path points, 685 walking connections, 247m walking route (matching Implementation Screenshot 1).
  - `AI Campus Assistant`: Quick questions buttons (matching Implementation Screenshot 2).
  - `Campus & Emergency Services`: **Your core module with the 5 features** (matching Implementation Screenshot 3).
  - `Campus Issue Reporting`: Maintenance requests.

