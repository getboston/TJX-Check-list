import streamlit as st
from datetime import datetime

# Configure page to look like a clean mobile app
st.set_page_config(page_title="TJX Server Refresh", page_icon="✔", layout="centered")

# App Styling & Branding
st.markdown("""
    <div style="background-color: #003366; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: white; text-align: center;">
        <h2 style="margin: 0; font-size: 20px; color: white;">TJX SERVER REFRESH</h2>
        <p style="margin: 3px 0 0 0; font-size: 12px; color: #cbd5e1; font-style: italic;">Form: DC-TCL-01 | Rev: 2026.1</p>
    </div>
""", unsafe_allow_html=True)

# Checklist Structure
sections = {
    "1. Store Arrival & Communication": [
        "Notify Barrister of exact arrival time.",
        "Send arrival email to CC@TJX.COM (CC: Mary, Katarina, Milos).",
        "Join the Barrister-provided Teams chat link when instructed.",
        "Provide store Manager on Duty with the TJX security code.",
        "Locate all TJX-provided equipment onsite before starting."
    ],
    "2. Onsite Inventory Verification": [
        "Verify HP DL380 Gen 11 Server (1 present).",
        "Verify Return Server Boxes (2 present - Note: 1 holds the Gen 11 HV Server).",
        "Verify USB Hard Drive(s) are present.",
        "Verify Rails (2 Server-Side, 2 Rack mounting).",
        "Verify Server Power Cords (2) and Pre-made Cable Labels.",
        "Verify extra rack screws/nuts are available."
    ],
    "3. Photo Documentation": [
        "Take pictures of the entire inventory BEFORE opening any boxes.",
        "Take pictures throughout the install as requested by the TJX Agent.",
        "Take pictures of all installed equipment after completion.",
        "Take a clear picture of the final return shipping label."
    ],
    "4. External Drive Removal & Shipping": [
        "Wait for Command Center instruction, then remove external drive from HV server.",
        "If drive packaging is missing, ask store management to provide it.",
        "Package drive and apply the FedEx label provided by the manager."
    ],
    "5. Fast Field Submission & Departure": [
        "Open the Fast Field Form link.",
        "Upload all required installation and shipping photos to the form.",
        "Submit the Fast Field form completely before leaving the site.",
        "Wait for explicit final approval from Barrister before departing."
    ]
}

# Quick Utilities Layout
st.subheader("🛠️ Quick Actions & Info")
col1, col2 = st.columns(2)
with col1:
    st.link_button("🚀 Launch Fast Field Form", "https://www.fastfieldwebforms.com/us/webforms/0142b3ee-b93a-472b-b97c-cdd6e682d43d", use_container_width=True)
with col2:
    st.info("📞 Support: 1-832-973-5221, Opt 1")

# Text copy helpers for mobile phones
st.caption("📱 Long-press code boxes below to copy emails directly on your phone:")
st.code("CC@TJX.COM")
st.code("Mary.Brannan@ncrvoyix.com, Katarina.Nikolic@ncrvoyix.com; Milos.Andric@ncrvoyix.com;")

st.write("---")

# Initialize app session state to keep track of checked states and timestamps
if "history" not in st.session_state:
    st.session_state.history = {}

total_tasks = sum(len(tasks) for tasks in sections.values())
completed_tasks = 0

# Render the interactive expandable checklist
st.subheader("📋 Deployment Checklist")
for sec_title, tasks in sections.items():
    with st.expander(sec_title, expanded=True):
        for task in tasks:
            # Unique identifier for state tracking
            state_key = f"check_{task}"
            
            # Draw standard checkbox
            checked = st.checkbox(task, key=state_key)
            
            if checked:
                completed_tasks += 1
                if task not in st.session_state.history:
                    st.session_state.history[task] = datetime.now().strftime("%I:%M:%S %p")
                st.markdown(f"<span style='color:#16a34a; font-size:12px;'>⏱️ Completed at {st.session_state.history[task]}</span>", unsafe_allow_html=True)
            else:
                if task in st.session_state.history:
                    del st.session_state.history[task]

st.write("---")

# Dynamic Progress Tracking Banner
progress_percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
st.subheader(f"📊 Deployment Progress: {progress_percent}%")
st.progress(progress_percent / 100)

if progress_percent == 100:
    st.balloons()
    st.success("🎉 All Onsite Tasks Completed & Verified!")

# Output Text Activity Log
if st.session_state.history:
    st.subheader("📑 Running Activity Log")
    log_text = ""
    for task, timestamp in st.session_state.history.items():
        log_text += f"[{timestamp}] ✔ {task}\n"
    st.code(log_text, language="text")