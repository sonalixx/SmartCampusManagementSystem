
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="CampusConnect",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- LOAD CSS ----------------

css_path = Path("assets/style.css")

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# ---------------- SESSION STATE ----------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "student_name" not in st.session_state:
    st.session_state.student_name = "Student"

if "emergency_sent" not in st.session_state:
    st.session_state.emergency_sent = False

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ---------------- CALLBACK FUNCTIONS ----------------

def go_to(page_name):
    st.session_state.page = page_name


def activate_sos():
    st.session_state.emergency_sent = True
    st.session_state.page = "Alerts"


def dismiss_sos():
    st.session_state.emergency_sent = False


# ---------------- HEADER ----------------

st.markdown("""
<div class="app-header">
    <div>
        <h2>🎓 CampusConnect</h2>
        <p>Your Smart Campus Companion</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- NAVIGATION ----------------

page = st.radio(
    "Navigation",
    ["Home", "AI Assistant", "Navigate", "Alerts", "Profile"],
    horizontal=True,
    label_visibility="collapsed",
    key="page"
)

st.divider()


# ==================================================
# HOME PAGE
# ==================================================

if page == "Home":

    st.markdown(f"""
    <div class="welcome-card">
        <p>WELCOME BACK</p>
        <h1>Hello, {st.session_state.student_name} 👋</h1>
        <p>Everything on campus, in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Campus Services")

    col1, col2 = st.columns(2)

    with col1:

        st.button(
            "🤖 AI Assistant",
            use_container_width=True,
            on_click=go_to,
            args=("AI Assistant",)
        )

        st.button(
            "📍 Campus Navigation",
            use_container_width=True,
            on_click=go_to,
            args=("Navigate",)
        )

    with col2:

        st.button(
            "📅 Campus Information",
            use_container_width=True,
            on_click=go_to,
            args=("AI Assistant",)
        )

        st.button(
            "🔔 Notifications",
            use_container_width=True,
            on_click=go_to,
            args=("Alerts",)
        )

    st.subheader("Emergency Assistance")

    st.button(
        "🚨 EMERGENCY SOS",
        type="primary",
        use_container_width=True,
        on_click=activate_sos
    )

    st.info(
        "Use the AI Assistant to ask questions "
        "about your campus."
    )


# ==================================================
# AI ASSISTANT
# ==================================================

elif page == "AI Assistant":

    st.title("🤖 AI Campus Assistant")

    st.caption("Ask me anything about your campus.")

    st.markdown("""
    <div class="info-card">
        <b>Try asking:</b><br><br>
        • When is my next exam?<br>
        • Where is the library?<br>
        • What is my attendance?<br>
        • Where is the AI department?
    </div>
    """, unsafe_allow_html=True)

    # Display previous messages

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input

    prompt = st.chat_input(
        "Ask your campus assistant..."
    )

    if prompt:

        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    from modules.chatbot import get_chat_response

                    response = get_chat_response(
                        prompt,
                        student_id="STU001"
                    )

                except ImportError:

                    response = (
                        "The AI backend is not connected yet. "
                        "Please try again after integration."
                    )

                except Exception:

                    response = (
                        "Sorry, something went wrong. "
                        "Please try again."
                    )

                st.write(response)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })


# ==================================================
# CAMPUS NAVIGATION
# ==================================================

elif page == "Navigate":

    st.title("📍 Campus Navigation")

    st.write(
        "Where are you and where do you want to go?"
    )

    locations = [
        "Main Gate",
        "Library",
        "AI Department",
        "Cafeteria",
        "Administrative Block",
        "Auditorium",
        "Computer Science Block"
    ]

    source = st.selectbox(
        "Your current location",
        locations
    )

    destination = st.selectbox(
        "Your destination",
        locations,
        index=2
    )

    if st.button(
        "Find My Route",
        use_container_width=True
    ):

        if source == destination:

            st.warning(
                "You are already at your destination!"
            )

        else:

            st.success("Route request created!")

            st.markdown(f"""
            <div class="info-card">
                <h3>🧭 Your Journey</h3>
                <p><b>Starting point:</b> {source}</p>
                <p>⬇️ Follow the campus pathway</p>
                <p><b>Destination:</b> {destination}</p>
            </div>
            """, unsafe_allow_html=True)

            st.info(
                "Sample route display. Connect the navigation "
                "module to generate actual campus pathways."
            )


# ==================================================
# ALERTS AND EMERGENCY
# ==================================================

elif page == "Alerts":

    st.title("🔔 Notifications & Emergency")

    if st.session_state.emergency_sent:

        st.error(
            "🚨 SOS demonstration activated! "
            "No real emergency notification has been sent."
        )

        st.button(
            "Dismiss SOS",
            on_click=dismiss_sos
        )

    st.subheader("Campus Notifications")

    st.markdown("""
    <div class="info-card">
        📢 <b>Campus Announcement</b>
        <p>Check the updated academic schedule.</p>
    </div>

    <div class="info-card">
        📅 <b>Examination Update</b>
        <p>Examination information is available in the student portal.</p>
    </div>

    <div class="info-card">
        🏫 <b>Campus Update</b>
        <p>Welcome to CampusConnect.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Report an Emergency")

    incident = st.selectbox(
        "Select emergency type",
        ["Medical", "Fire", "Security", "Other"]
    )

    description = st.text_area(
        "Describe the situation"
    )

    if st.button(
        "Submit Report",
        use_container_width=True
    ):

        if description.strip():

            st.success(
                "Demo report created. Connect Supabase "
                "to store and notify campus authorities."
            )

        else:

            st.warning(
                "Please enter a description."
            )


# ==================================================
# STUDENT PROFILE
# ==================================================

elif page == "Profile":

    st.title("👤 Student Profile")

    name = st.text_input(
        "Student Name",
        value=st.session_state.student_name
    )

    student_id = st.text_input(
        "Student ID",
        value="STU001"
    )

    department = st.selectbox(
        "Department",
        ["AIML", "CSE", "ECE", "ISE", "Mechanical"]
    )

    semester = st.selectbox(
        "Semester",
        ["1", "2", "3", "4", "5", "6", "7", "8"],
        index=4
    )

    if st.button(
        "Save Profile",
        use_container_width=True
    ):

        st.session_state.student_name = name

        st.success("Profile updated!")

    st.write("Student ID:", student_id)
    st.write("Department:", department)
    st.write("Semester:", semester)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
    '<p class="footer">CampusConnect © 2026 | '
    'Smart Campus Management System</p>',
    unsafe_allow_html=True
)
