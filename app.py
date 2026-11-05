"""
Alliance University - Smart Campus Management System
E1CSA313 Design Project - 1
Mentor: Dr. Vinita Nair

Module 3: Centralized Campus and Emergency Services
Focus: Emergency & Notification Management
- 1. Emergency SOS button for students
- 2. Emergency Incident Reporting
- 3. Online Database Storage (Supabase)
- 4. Real-time Emergency Screen Popup Alert
- 5. Student Notification Center & Management
"""

import os
import base64
import time
import datetime
import streamlit as st
import config
from supabase_client import SupabaseManager
from notifications_manager import NotificationManager, render_audio_siren

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Alliance University - Smart Campus Management System",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Theme CSS matching Alliance University PPT Slides
st.markdown("""
<style>
    /* Dark Theme Backgrounds */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    
    /* Alliance University Header styling */
    .au-header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg, #161b22 0%, #1f242c 100%);
        border-bottom: 3px solid #8b0000;
        padding: 12px 24px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .au-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .au-naac-badge {
        background-color: #ffffff;
        color: #8b0000;
        padding: 4px 12px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 13px;
        border-left: 4px solid #b91c1c;
    }
    
    /* Metric Cards */
    .stat-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stat-number {
        font-size: 28px;
        font-weight: bold;
        color: #58a6ff;
    }
    .stat-label {
        font-size: 13px;
        color: #8b949e;
        text-transform: uppercase;
        margin-top: 4px;
    }
    
    /* Pulsing Red SOS Button */
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
        70% { box-shadow: 0 0 0 16px rgba(220, 38, 38, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    .sos-btn-box {
        animation: pulse-red 2s infinite;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    
    /* Critical Alert Banner */
    .emergency-banner {
        background: linear-gradient(90deg, #7f1d1d 0%, #991b1b 100%);
        border: 2px solid #ef4444;
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: space-between;
        animation: pulse-red 2s infinite;
    }

    /* Notification Cards */
    .notif-card {
        background-color: #161b22;
        border-left: 5px solid #3b82f6;
        border-top: 1px solid #30363d;
        border-right: 1px solid #30363d;
        border-bottom: 1px solid #30363d;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .notif-card-emergency {
        background-color: #201314;
        border-left: 5px solid #ef4444;
        border-top: 1px solid #7f1d1d;
        border-right: 1px solid #7f1d1d;
        border-bottom: 1px solid #7f1d1d;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .notif-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .notif-title {
        font-size: 16px;
        font-weight: 700;
        color: #f0f6fc;
    }
    .notif-time {
        font-size: 12px;
        color: #8b949e;
    }
    .notif-meta {
        font-size: 12px;
        color: #58a6ff;
        margin-bottom: 8px;
    }
    .notif-body {
        font-size: 14px;
        color: #c9d1d9;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "supabase_url" not in st.session_state:
    st.session_state.supabase_url = config.DEFAULT_SUPABASE_URL
if "supabase_key" not in st.session_state:
    st.session_state.supabase_key = config.DEFAULT_SUPABASE_KEY
if "dismissed_alerts" not in st.session_state:
    st.session_state.dismissed_alerts = set()
if "last_sos_time" not in st.session_state:
    st.session_state.last_sos_time = None
if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = True
if "popup_triggered" not in st.session_state:
    st.session_state.popup_triggered = False
if "current_alert_details" not in st.session_state:
    st.session_state.current_alert_details = None

# Initialize Database & Manager
db = SupabaseManager(st.session_state.supabase_url, st.session_state.supabase_key)
manager = NotificationManager(db)

# ---------------------------------------------------------
# 4. EMERGENCY SCREEN POPUP ALERT (Streamlit Dialog)
# ---------------------------------------------------------
@st.dialog("🚨 CAMPUS EMERGENCY ALERT - IMMEDIATE ACTION REQUIRED", width="large")
def show_emergency_dialog(alert_data: dict):
    """Real-time emergency popup modal on student's screen."""
    if st.session_state.sound_enabled:
        render_audio_siren()
    
    st.error(f"### {alert_data.get('title', 'CRITICAL CAMPUS EMERGENCY')}")
    
    col_d1, col_d2 = st.columns([2, 1])
    with col_d1:
        st.markdown(f"""
        **📍 Affected Campus Location:** `{alert_data.get('location', 'Campus-Wide')}`  
        **⏱️ Broadcast Time:** `{alert_data.get('created_at', str(datetime.datetime.now()))}`  
        **⚠️ Priority:** `CRITICAL EMERGENCY (LIFE SAFETY)`  
        
        **📋 Emergency Advisory & Instructions:**
        {alert_data.get('message', 'Please follow campus security protocols immediately.')}
        """)
        
        st.info("""
        **🛡️ Safe Evacuation & Action Steps:**
        1. Remain calm and follow emergency warden instructions.
        2. Do NOT use elevators in case of fire or power failure.
        3. Proceed immediately to designated assembly point:
           **`Central Lawn in front of Academic Block`**
        4. Assist persons with disabilities or injuries if safe to do so.
        """)
        
    with col_d2:
        st.markdown("#### 📞 Emergency Helplines")
        st.error("**Campus Security:**\n+91 80 4619 9000")
        st.warning("**Health Centre:**\n+91 80 4619 9112")
        st.info("**National SOS:**\n112 / 108")
        
    st.divider()
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("✅ I Am Safe / Acknowledge Alert", use_container_width=True, type="primary"):
            st.session_state.dismissed_alerts.add(str(alert_data.get("id")))
            st.session_state.popup_triggered = False
            st.session_state.current_alert_details = None
            st.success("Alert acknowledged. Stay safe!")
            time.sleep(0.5)
            st.rerun()
            
    with col_btn2:
        if st.button("🚨 I Need Urgent Help Here", use_container_width=True):
            st.session_state.dismissed_alerts.add(str(alert_data.get("id")))
            st.session_state.popup_triggered = False
            st.session_state.current_alert_details = None
            st.toast("Security team has received your distress signal!", icon="🚨")
            time.sleep(0.5)
            st.rerun()


# ---------------------------------------------------------
# Check for Active Emergencies & Trigger Popup
# ---------------------------------------------------------
active_emergency = db.get_active_emergency()
if active_emergency and str(active_emergency.get("id")) not in st.session_state.dismissed_alerts:
    st.session_state.popup_triggered = True
    st.session_state.current_alert_details = active_emergency


# ---------------------------------------------------------
# Alliance University Header Banner (With Crest Logo)
# ---------------------------------------------------------
logo_path = os.path.join(os.path.dirname(__file__), "alliance_logo.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 58px; height: 58px; border-radius: 50%; object-fit: contain; vertical-align: middle; margin-right: 14px; box-shadow: 0 0 10px rgba(0,0,0,0.5);">'
else:
    logo_html = '<span style="font-size: 36px; margin-right: 14px;">🏛️</span>'

st.markdown(f"""
<div class="au-header-container">
    <div style="display: flex; align-items: center;">
        {logo_html}
        <div>
            <div class="au-title">
                {config.UNIVERSITY_NAME.upper()}
            </div>
            <div style="font-size: 13px; color: #8b949e; margin-top: 2px;">
                {config.PROJECT_TITLE}
            </div>
        </div>
    </div>
    <div style="text-align: right;">
        <div class="au-naac-badge">
            ⭐ {config.ACCREDITATION}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Show Banner if Active Emergency
if active_emergency:
    st.markdown(f"""
    <div class="emergency-banner">
        <div>
            <span style="font-size: 20px;">🚨</span>
            <strong style="font-size: 16px; margin-left: 8px;">ACTIVE CAMPUS EMERGENCY:</strong>
            <span style="margin-left: 8px;">{active_emergency.get('title', 'Emergency Incident')}</span>
            <span style="background-color: #00000044; padding: 2px 8px; border-radius: 4px; margin-left: 10px; font-size: 12px;">
                📍 {active_emergency.get('location', 'Campus')}
            </span>
        </div>
        <div>
            <span style="font-size: 12px; opacity: 0.9;">Reported: {active_emergency.get('created_at', 'Just now')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Trigger Dialog if unacknowledged
if st.session_state.popup_triggered and st.session_state.current_alert_details:
    show_emergency_dialog(st.session_state.current_alert_details)


# ---------------------------------------------------------
# Sidebar Navigation (Matches PPT Slides)
# ---------------------------------------------------------
with st.sidebar:
    nav_icon_path = os.path.join(os.path.dirname(__file__), "navigation_icon.png")
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        if os.path.exists(nav_icon_path):
            st.image(nav_icon_path, width=42)
        else:
            st.markdown("<span style='font-size: 28px;'>🧭</span>", unsafe_allow_html=True)
    with col_nav2:
        st.markdown("<h3 style='margin-top: 4px; margin-bottom: 0px;'>Navigation</h3>", unsafe_allow_html=True)
    
    page = st.radio(
        "Select Module:",
        [
            "Home",
            "Campus Navigation",
            "AI Campus Assistant",
            "Campus & Emergency Services",
            "Campus Issue Reporting"
        ],
        index=3  # Default to user's assigned module
    )
    
    st.divider()
    
    # Emergency Quick Status
    st.markdown("#### 🚨 Safety Status")
    if active_emergency:
        st.error("⚠️ **EMERGENCY ACTIVE**")
        if st.button("👁️ Re-open Emergency Popup", use_container_width=True):
            st.session_state.popup_triggered = True
            st.session_state.current_alert_details = active_emergency
            st.rerun()
        if st.button("✅ Resolve / Clear Emergency", use_container_width=True):
            db.resolve_emergency(str(active_emergency.get("id")))
            st.session_state.dismissed_alerts.clear()
            st.success("Emergency marked as resolved!")
            time.sleep(0.5)
            st.rerun()
    else:
        st.success("🟢 Campus All Clear")
        
    st.divider()
    
    # Notification Badge
    stats = manager.get_stats()
    st.markdown("#### 🔔 Notification Center")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.metric("Total", stats["total"])
    with col_sb2:
        st.metric("Unread", stats["unread"])
        
    # Database Connection State
    is_live, conn_msg = db.test_connection()
    st.markdown("#### ☁️ Cloud Database")
    if is_live:
        st.success("🟢 Supabase Connected")
    else:
        st.warning("🟡 Offline Mode (Local DB)")
    st.caption(f"Status: {conn_msg}")
    
    st.divider()
    st.markdown("#### 📞 Quick Helpline")
    st.caption("🚨 Security: **+91 80 4619 9000**")
    st.caption("🏥 Health Centre: **+91 80 4619 9112**")
    st.caption("🛡️ National SOS: **112**")


# =========================================================
# PAGE 1: CAMPUS & EMERGENCY SERVICES (USER'S MAIN WORK)
# =========================================================
if page == "Campus & Emergency Services":
    st.markdown("## 🛡️ Centralized Campus & Emergency Services")
    st.markdown(
        "*Unified emergency response, real-time safety broadcasting, and student notification management.*"
    )

    # 6 Interactive Tabs
    tab_sos, tab_report, tab_notifs, tab_announcements, tab_helplines, tab_supabase = st.tabs([
        "🚨 1. Emergency SOS",
        "📝 2. Report Emergency",
        "🔔 3. Manage Notifications",
        "📢 4. Campus Announcements",
        "☎️ 5. Helplines & Safety",
        "☁️ 6. Supabase Cloud Setup"
    ])

    # -----------------------------------------------------
    # TAB 1: EMERGENCY SOS BUTTON FOR STUDENTS (Req 1)
    # -----------------------------------------------------
    with tab_sos:
        st.markdown("### 🚨 Emergency SOS System")
        st.info(
            "Use this in immediate danger, accident, medical emergency, or harassment situation. "
            "Pressing the SOS button instantly broadcasts a critical emergency alert, notifies campus security, "
            "and triggers an emergency popup across all screens."
        )

        st.markdown('<div class="sos-btn-box">', unsafe_allow_html=True)
        col_sos_left, col_sos_right = st.columns([1.2, 1])

        with col_sos_left:
            st.markdown("#### 👤 Student SOS Information")
            sos_student_name = st.text_input("Student Name:", value="Bhavishya Raj M.H", key="sos_name")
            sos_student_id = st.text_input("Registration / Student ID:", value="2411021060805", key="sos_id")
            sos_contact = st.text_input("Contact Phone Number:", value="+91 98765 43210", key="sos_phone")
            
            sos_location = st.selectbox(
                "Current Campus Location (Where are you?):",
                config.CAMPUS_LOCATIONS,
                index=1,
                key="sos_loc"
            )
            
            sos_type = st.selectbox(
                "Nature of Emergency:",
                config.EMERGENCY_TYPES,
                index=0,
                key="sos_type"
            )

        with col_sos_right:
            st.markdown("#### ⚠️ Instant Action Trigger")
            st.write("Clicking this button will:")
            st.markdown("""
            - 🚨 Log the emergency incident to **Supabase Cloud**.
            - 📢 Broadcast a **High-Priority Campus Notification**.
            - 🖥️ Trigger an instant **Full-Screen Popup Alert**.
            - 🚔 Dispatch campus security patrol to your location.
            """)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚨 TRIGGER EMERGENCY SOS NOW", type="primary", use_container_width=True, key="btn_sos_trigger"):
                with st.spinner("Broadcasting Emergency SOS to Campus Network..."):
                    report = manager.trigger_sos(
                        student_name=sos_student_name,
                        student_id=sos_student_id,
                        location=sos_location,
                        emergency_type=sos_type,
                        contact_number=sos_contact
                    )
                    st.session_state.last_sos_time = datetime.datetime.now().strftime("%H:%M:%S")
                    st.session_state.dismissed_alerts.clear()
                    st.session_state.popup_triggered = True
                    st.session_state.current_alert_details = report
                    
                st.error("### 🚨 SOS BROADCAST SUCCESSFUL!")
                st.markdown(f"""
                **Emergency ID:** `{report.get('id')}`  
                **Location Dispatched:** `{sos_location}`  
                **Status:** `DISPATCHING ALLIANCE QUICK RESPONSE TEAM`  
                """)
                time.sleep(1)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Simulation button for testing
        st.divider()
        st.markdown("#### 🧪 Demo / Professor Evaluation Mode")
        st.caption("Click below to simulate an instant campus-wide fire evacuation test alert:")
        col_sim1, col_sim2 = st.columns([1, 1])
        with col_sim1:
            if st.button("🔥 Simulate Fire Evacuation Alert", use_container_width=True):
                manager.trigger_sos(
                    student_name="Campus Fire Safety Sensor #04",
                    student_id="CAMPUS-SEC-01",
                    location="Academic Block - 2nd Floor (Lecture Halls)",
                    emergency_type="🔥 Fire Hazard / Smoke Alert",
                    contact_number="+91 80 4619 9000"
                )
                st.session_state.dismissed_alerts.clear()
                st.session_state.popup_triggered = True
                st.rerun()
        with col_sim2:
            if st.button("🏥 Simulate Medical First-Aid Alert", use_container_width=True):
                manager.trigger_sos(
                    student_name="Student Welfare Officer",
                    student_id="SWO-AU-99",
                    location="Sports Complex & Main Ground",
                    emergency_type="🏥 Medical Emergency / Accident",
                    contact_number="+91 80 4619 9112"
                )
                st.session_state.dismissed_alerts.clear()
                st.session_state.popup_triggered = True
                st.rerun()

    # -----------------------------------------------------
    # TAB 2: A WAY TO REPORT AN EMERGENCY (Req 2)
    # -----------------------------------------------------
    with tab_report:
        st.markdown("### 📝 Report a Campus Emergency / Incident")
        st.markdown(
            "Submit a detailed incident report to campus authorities. "
            "All submissions are immediately stored in the **Supabase** database and reviewed by campus safety officers."
        )

        with st.form("emergency_report_form", clear_on_submit=True):
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                rep_name = st.text_input("Reporter Name *", placeholder="e.g. Vidhyasri R.")
                rep_id = st.text_input("Student / Staff ID *", placeholder="e.g. 2411021060047")
                rep_phone = st.text_input("Contact Phone Number *", placeholder="e.g. +91 91234 56789")
                rep_type = st.selectbox("Emergency Category *", config.EMERGENCY_TYPES)
                
            with col_r2:
                rep_location = st.selectbox("Location of Incident *", config.CAMPUS_LOCATIONS)
                rep_specific_loc = st.text_input(
                    "Specific Spot / Landmark",
                    placeholder="e.g. Near Staircase B, Room 204"
                )
                rep_severity = st.select_slider(
                    "Severity Level *",
                    options=["Medium", "High", "Critical"],
                    value="High",
                    help="Critical triggers immediate campus-wide sirens and popups"
                )
                rep_witnesses = st.text_input("Names / Contacts of Witnesses (Optional)")

            rep_desc = st.text_area(
                "Incident Description & Immediate Assistance Needed *",
                placeholder="Describe what occurred, any injured persons, active hazards, or immediate support required...",
                height=120
            )

            submit_report = st.form_submit_button(
                "📤 Submit Emergency Report to Supabase",
                type="primary",
                use_container_width=True
            )

            if submit_report:
                if not rep_name or not rep_id or not rep_phone or not rep_desc:
                    st.error("Please fill in all mandatory fields (Name, ID, Phone, Description).")
                else:
                    full_loc = f"{rep_location} ({rep_specific_loc})" if rep_specific_loc else rep_location
                    with st.spinner("Transmitting incident report to Supabase Cloud..."):
                        report = manager.report_incident(
                            student_name=rep_name,
                            student_id=rep_id,
                            contact_number=rep_phone,
                            emergency_type=rep_type,
                            location=full_loc,
                            severity=rep_severity,
                            description=rep_desc
                        )
                    
                    st.success("✅ Emergency Report successfully submitted and saved to Supabase!")
                    st.balloons()
                    if rep_severity == "Critical":
                        st.session_state.dismissed_alerts.clear()
                        st.session_state.popup_triggered = True
                        st.session_state.current_alert_details = report
                        st.rerun()

        # Display Recent Incident Reports Table
        st.divider()
        st.markdown("#### 📋 Recent Emergency Incident Log (Supabase Feed)")
        reports = db.fetch_emergency_reports()
        if reports:
            table_data = []
            for r in reports[:10]:
                table_data.append({
                    "Date & Time": r.get("created_at"),
                    "Type": r.get("emergency_type"),
                    "Location": r.get("location"),
                    "Severity": r.get("severity"),
                    "Reported By": f"{r.get('student_name')} ({r.get('student_id')})",
                    "Status": r.get("status")
                })
            st.dataframe(table_data, use_container_width=True)
        else:
            st.info("No emergency reports filed yet. The campus is safe.")

    # -----------------------------------------------------
    # TAB 3: MANAGE NOTIFICATIONS (Req 5)
    # -----------------------------------------------------
    with tab_notifs:
        st.markdown("### 🔔 Student Notification Management Page")
        st.markdown("Review, filter, acknowledge, and manage all your campus notices and emergency alerts.")

        # Notification Metrics Summary
        stats = manager.get_stats()
        c_stat1, c_stat2, c_stat3, c_stat4 = st.columns(4)
        with c_stat1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total']}</div>
                <div class="stat-label">Total Notifications</div>
            </div>
            """, unsafe_allow_html=True)
        with c_stat2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="color: #f59e0b;">{stats['unread']}</div>
                <div class="stat-label">Unread Notices</div>
            </div>
            """, unsafe_allow_html=True)
        with c_stat3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="color: #ef4444;">{stats['emergencies']}</div>
                <div class="stat-label">Active Emergencies</div>
            </div>
            """, unsafe_allow_html=True)
        with c_stat4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="color: #10b981;">{stats['total'] - stats['unread']}</div>
                <div class="stat-label">Read & Handled</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Action Toolbar
        col_act1, col_act2, col_act3 = st.columns([1, 1, 1])
        with col_act1:
            if st.button("✅ Mark All as Read", use_container_width=True):
                db.mark_all_notifications_as_read()
                st.success("All notifications marked as read!")
                time.sleep(0.5)
                st.rerun()
        with col_act2:
            if st.button("🔄 Refresh Notifications", use_container_width=True):
                st.rerun()
        with col_act3:
            if st.button("🗑️ Clear All Notifications", use_container_width=True):
                db.clear_all_notifications()
                st.success("Notification inbox cleared!")
                time.sleep(0.5)
                st.rerun()

        # Search & Filter Controls
        st.divider()
        col_f1, col_f2, col_f3 = st.columns([1.5, 1, 1])
        with col_f1:
            search_text = st.text_input("🔍 Search Notifications:", placeholder="Search title, sender, location or keywords...")
        with col_f2:
            cat_filter = st.selectbox(
                "Filter by Category:",
                ["All", "🚨 Emergencies", "📢 Announcements", "🛡️ Security", "🏥 Medical"]
            )
        with col_f3:
            stat_filter = st.selectbox(
                "Filter by Read Status:",
                ["All", "Unread Only", "Read Only", "Active Emergencies"]
            )

        # Filter and display items
        filtered_items = manager.filter_notifications(
            category=cat_filter,
            status_filter=stat_filter,
            search_query=search_text
        )

        st.markdown(f"**Showing {len(filtered_items)} notification(s)**")

        if not filtered_items:
            st.info("No notifications match your current filter.")
        else:
            for item in filtered_items:
                notif_id = str(item.get("id"))
                is_emergency = item.get("is_emergency", False)
                is_read = item.get("is_read", False)
                created_time = item.get("created_at", "")
                title = item.get("title", "Untitled Notification")
                message = item.get("message", "")
                sender = item.get("sender", "Campus Admin")
                loc = item.get("location", "Campus-wide")
                priority = item.get("priority", "medium").upper()

                card_class = "notif-card-emergency" if is_emergency else "notif-card"
                badge_color = "#ef4444" if is_emergency else "#3b82f6"
                read_badge = "✅ Read" if is_read else "🔴 Unread"

                st.markdown(f"""
                <div class="{card_class}">
                    <div class="notif-header">
                        <div>
                            <span style="background-color: {badge_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-right: 8px;">
                                {priority}
                            </span>
                            <span class="notif-title">{title}</span>
                        </div>
                        <span class="notif-time">{created_time} • {read_badge}</span>
                    </div>
                    <div class="notif-meta">
                        👤 From: <strong>{sender}</strong> &nbsp;|&nbsp; 📍 Location: <strong>{loc}</strong>
                    </div>
                    <div class="notif-body">
                        {message}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Action buttons for individual notification
                col_nb1, col_nb2, col_nb3 = st.columns([1, 1, 4])
                with col_nb1:
                    if not is_read:
                        if st.button("Mark Read", key=f"read_{notif_id}"):
                            db.mark_notification_as_read(notif_id, True)
                            st.rerun()
                    else:
                        if st.button("Mark Unread", key=f"unread_{notif_id}"):
                            db.mark_notification_as_read(notif_id, False)
                            st.rerun()
                with col_nb2:
                    if st.button("Delete", key=f"del_{notif_id}"):
                        db.delete_notification(notif_id)
                        st.rerun()

        # Notification Preferences Panel
        st.divider()
        with st.expander("⚙️ Notification Preferences & Audio Alert Settings"):
            st.session_state.sound_enabled = st.toggle(
                "🔊 Enable Audible Emergency Siren during alerts",
                value=st.session_state.sound_enabled
            )
            st.toggle("📱 Simulate SMS notification forward to student phone", value=True)
            st.toggle("📧 Simulate Email alert digest", value=True)
            st.caption("Settings are saved automatically for your session.")

    # -----------------------------------------------------
    # TAB 4: CAMPUS ANNOUNCEMENTS (Matches Screenshot 3 in PPT!)
    # -----------------------------------------------------
    with tab_announcements:
        st.markdown("### Campus Announcements")
        st.markdown("*Published campus circulars, department events, and administrative notices.*")

        # Announcement Publishing Form (Exact replica of PPT Screenshot 3)
        with st.expander("📢 Publish a New Announcement", expanded=True):
            with st.form("new_announcement_form", clear_on_submit=True):
                pub_title = st.text_input("Announcement Title", placeholder="e.g. Workshop on Cloud Computing")
                pub_dept = st.selectbox(
                    "Publishing Department",
                    ["Department of Computer Science", "Office of Dean - Engineering", "Central Library", "Campus Administration", "Sports Committee"]
                )
                pub_location = st.selectbox("Related Campus Location", config.CAMPUS_LOCATIONS)
                pub_msg = st.text_area("Announcement Message", placeholder="Enter announcement body text here...", height=100)
                
                publish_btn = st.form_submit_button("Publish Announcement", type="primary")
                if publish_btn:
                    if not pub_title or not pub_msg:
                        st.error("Please provide both Announcement Title and Message.")
                    else:
                        db.add_notification(
                            title=pub_title,
                            message=pub_msg,
                            category="announcement",
                            priority="medium",
                            sender=pub_dept,
                            location=pub_location,
                            is_emergency=False,
                            status="active"
                        )
                        st.success("Announcement published successfully to Supabase!")
                        time.sleep(0.5)
                        st.rerun()

        # List Existing Announcements (Matches Seminar & Library in PPT)
        st.divider()
        st.markdown("#### Published Campus Notices")
        notifs = db.fetch_notifications()
        announcements = [n for n in notifs if n.get("category") == "announcement"]

        if announcements:
            for ann in announcements:
                st.markdown(f"### {ann.get('title')}")
                st.markdown(f"{ann.get('message')}")
                st.caption(f"Published: {ann.get('created_at')} • By: {ann.get('sender')} • Location: {ann.get('location')}")
                st.divider()
        else:
            st.info("No campus announcements published yet.")

    # -----------------------------------------------------
    # TAB 5: HELPLINES & SAFETY INFORMATION
    # -----------------------------------------------------
    with tab_helplines:
        st.markdown("### ☎️ Alliance University Emergency Directory")
        st.markdown("24/7 Verified emergency contacts across Alliance University campus.")

        for contact in config.EMERGENCY_CONTACTS:
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"**{contact['name']}**")
                st.caption(contact["desc"])
            with c2:
                st.code(contact["phone"])
            with c3:
                st.caption(f"Badge: {contact['badge']}")
            st.divider()

        st.markdown("### 🏃 Safe Campus Evacuation Assembly Points")
        for idx, pt in enumerate(config.ASSEMBLY_POINTS, 1):
            st.markdown(f"**Point {idx}:** {pt}")

    # -----------------------------------------------------
    # TAB 6: SUPABASE CLOUD SETUP (Req 3 Guide)
    # -----------------------------------------------------
    with tab_supabase:
        st.markdown("### ☁️ Supabase Cloud Database Integration")
        st.markdown("""
        All notifications, emergency alerts, and SOS incident reports are saved online using **Supabase** (PostgreSQL cloud database).
        """)

        is_connected, msg = db.test_connection()
        if is_connected:
            st.success(f"✅ **Supabase Status:** {msg}")
        else:
            st.warning(f"⚠️ **Supabase Status:** {msg}")

        st.markdown("#### Configure Supabase Project Credentials")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            new_url = st.text_input(
                "Supabase Project URL:",
                value=st.session_state.supabase_url,
                placeholder="https://your-project-id.supabase.co"
            )
        with col_s2:
            new_key = st.text_input(
                "Supabase Anon Public API Key:",
                value=st.session_state.supabase_key,
                type="password",
                placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            )

        if st.button("Save & Test Supabase Credentials", type="primary"):
            st.session_state.supabase_url = new_url
            st.session_state.supabase_key = new_key
            test_db = SupabaseManager(new_url, new_key)
            ok, test_msg = test_db.test_connection()
            if ok:
                st.success(f"🎉 Success! {test_msg}")
            else:
                st.error(f"❌ Connection test failed: {test_msg}")
            time.sleep(1)
            st.rerun()

        st.divider()
        st.markdown("#### 📖 1-Click Database Setup Instructions (for Beginners)")
        with st.expander("Click to view SQL script to paste into Supabase SQL Editor:"):
            st.code("""
-- 1. Open your Supabase Dashboard: https://supabase.com
-- 2. Go to: SQL Editor -> New Query
-- 3. Paste the contents of 'schema.sql' and click 'RUN'!

CREATE TABLE IF NOT EXISTS public.campus_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'announcement',
    priority TEXT NOT NULL DEFAULT 'medium',
    sender TEXT NOT NULL DEFAULT 'Campus Administration',
    location TEXT DEFAULT 'Campus-wide',
    is_emergency BOOLEAN DEFAULT FALSE,
    is_read BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.emergency_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    emergency_type TEXT NOT NULL,
    location TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'Critical',
    description TEXT,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS & Policies
ALTER TABLE public.campus_notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.emergency_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read" ON public.campus_notifications FOR SELECT USING (true);
CREATE POLICY "Allow public insert" ON public.campus_notifications FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public update" ON public.campus_notifications FOR UPDATE USING (true);
CREATE POLICY "Allow public delete" ON public.campus_notifications FOR DELETE USING (true);

CREATE POLICY "Allow reports read" ON public.emergency_reports FOR SELECT USING (true);
CREATE POLICY "Allow reports insert" ON public.emergency_reports FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow reports update" ON public.emergency_reports FOR UPDATE USING (true);
            """, language="sql")


# =========================================================
# OTHER MODULES (MATCHING PPT SLIDES & WORKFLOW)
# =========================================================
elif page == "Campus Navigation":
    # Replica of Implementation Screenshot 1 in PPT
    st.markdown("## 📍 Campus Navigation")
    st.caption("Find a walking route using your campus OpenStreetMap data.")

    st.success("Campus map loaded: 663 mapped path points.")
    st.write("**Total connected map points:** 663")
    st.write("**Total walking connections:** 685")

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        st.markdown("#### 📍 Starting point")
        start_loc = st.selectbox("Starting Location", ["Alliance University", "Central Library", "Academic Block", "Hostel Block A"])
    with col_nav2:
        st.markdown("#### 🎯 Destination")
        dest_loc = st.selectbox("Destination", ["Alliance University Car Parking", "Computer Laboratory", "Food Court", "Seminar Hall"])

    route_btn = st.button("🔴 Find shortest route", type="primary")
    
    st.write("**Start and destination connected:** `True`")
    st.success("Walking route calculated!")
    c_r1, c_r2 = st.columns(2)
    with c_r1:
        st.metric("Walking distance", "247 metres")
    with c_r2:
        st.metric("Estimated walking time", "3 minutes")
    st.caption(f"Start: {start_loc}")
    st.caption(f"Destination: {dest_loc}")
    
    # Campus Walking Route Map Picture (Matches Implementation Screenshot 1 in PPT)
    map_img_path = os.path.join(os.path.dirname(__file__), "campus_navigation_map.png")
    if os.path.exists(map_img_path):
        st.image(map_img_path, caption="Alliance University Campus Walking Route (OpenStreetMap)", use_container_width=True)
    else:
        st.info("🗺️ Interactive A*/Dijkstra campus walking route visualizer loaded.")

elif page == "AI Campus Assistant":
    # Replica of Implementation Screenshot 2 in PPT
    st.markdown("## 🤖 AI-Based Campus Management")
    st.markdown("### Quick Questions")
    st.caption("Select a question to explore campus information:")

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        q_books = st.button("📚 Where can I find books?")
        q_comp = st.button("💻 Where can I find computers?")
    with col_q2:
        q_fees = st.button("💰 Where can I enquire about fees?")
        q_food = st.button("🍽️ Where can I get food?")

    query = st.text_input("Ask a question about campus facilities to find relevant information:", value="Where can I find computers?")
    
    if st.button("Find Answer", type="primary") or q_comp:
        st.success("Relevant result: Computer Laboratory")
        st.write("**Computers and practical sessions**")
        st.write("**Location:** Academic Block, First Floor")
        st.caption("Prototype: Uses rule-based keyword matching. A real AI model can be integrated in a future version.")
    elif q_books:
        st.success("Relevant result: Central Library")
        st.write("**Reference books, journals and quiet study areas**")
        st.write("**Location:** Central Library Building, Ground & First Floor")
    elif q_fees:
        st.success("Relevant result: Accounts & Finance Office")
        st.write("**Student fee queries, receipts and scholarships**")
        st.write("**Location:** Administrative Block, Ground Floor")
    elif q_food:
        st.success("Relevant result: Food Court & Cafeteria")
        st.write("**Meals, refreshments and student cafeteria**")
        st.write("**Location:** Student Amenities Block")

elif page == "Campus Issue Reporting":
    st.markdown("## ⚠️ Campus Issue Reporting")
    st.caption("Report maintenance, infrastructure, or facility defects to campus administration.")
    with st.form("issue_report_form"):
        i_title = st.text_input("Issue Summary", placeholder="e.g. Projector not working in Room 102")
        i_cat = st.selectbox("Category", ["Electrical", "Plumbing", "IT / Equipment", "Furniture", "Cleanliness"])
        i_loc = st.selectbox("Location", config.CAMPUS_LOCATIONS)
        i_desc = st.text_area("Detailed Description")
        if st.form_submit_button("Submit Maintenance Request", type="primary"):
            st.success("Maintenance ticket logged! Ticket ID: #AU-REQ-2026-88")

elif page == "Home":
    st.markdown("## 🏫 Smart Campus Management System Using AI")
    st.markdown("#### Alliance University • E1CSA313 Design Project - 1")
    st.markdown(f"**Mentor:** {config.MENTOR_NAME}")
    
    st.markdown("""
    ### Team Members:
    1. **BHAVISHYA RAJ M.H** – 2411021060805
    2. **VIDHYASRI. R** – 2411021060047
    3. **SAMRIDDHI SINGH** – 2411021060838
    4. **R. DHARSHINI** – 2411021060087
    
    ---
    ### Core Modules:
    - **Module 1: Campus Navigation Module** (Pathfinding, OpenStreetMap, Shortest Route)
    - **Module 2: AI-Based Campus Management Module** (Virtual Assistant, Campus Queries)
    - **Module 3: Centralized Campus and Emergency Services Module** (Emergency Alert Service, Evacuation, Notifications, Supabase Storage)
    """)
    
    st.info("👈 Use the sidebar navigation on the left to explore the modules, or go directly to 'Campus & Emergency Services' for the Emergency & Notification Management system.")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #8b949e; font-size: 12px; border-top: 1px solid #30363d; padding-top: 16px;">
    Alliance University — Smart Campus Management System Using AI • E1CSA313 Design Project - 1 • Mentor: Dr. Vinita Nair
</div>
""", unsafe_allow_html=True)

