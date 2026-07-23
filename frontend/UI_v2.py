import streamlit as st
import requests

# ----------------------------------
# Backend URL
# ----------------------------------

try:
    BACKEND_URL = st.secrets["BACKEND_URL"].rstrip("/")
except Exception:
    BACKEND_URL = "https://self-healing-two-production-2677.up.railway.app"

# ----------------------------------
# Page Config
# ----------------------------------

st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="🎓",
    layout="wide"
)

# ----------------------------------
# Session State
# ----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------
# Sidebar
# ----------------------------------

with st.sidebar:

    st.title("🎓 AI Academic Assistant")

    st.markdown("---")

    st.markdown("### Ask Questions About")

    st.markdown("""
- 📌 Admissions
- 💰 Fee Structure
- 🎓 Scholarships
- 👨‍🏫 Faculty
- 📅 Academic Calendar
- 📚 Study Material
- ⏰ Batch Timings
- 📝 Student Policies
- 🚀 JEE Preparation
- 🩺 NEET Preparation
""")

    st.markdown("---")

    # Backend Status
    try:

        health = requests.get(
            f"{BACKEND_URL}/health",
            timeout=5
        )

        if health.status_code == 200:
            st.success("Backend Connected")

        else:
            st.error("Backend Not Healthy")

    except:
        st.error("Backend Offline")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

# ----------------------------------
# Header
# ----------------------------------

st.title("🎓 AI Academic Assistant")

st.info(
    """
Ask questions related to your academic documents.

Examples:

• What is the JEE fee?

• Do you provide study material?

• What are the batch timings?

• How can I apply for admission?

• Tell me about scholarships.
"""
)

# ----------------------------------
# Display Chat History
# ----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# ----------------------------------
# Chat Input
# ----------------------------------

user_message = st.chat_input(
    "Ask your academic question..."
)

# ----------------------------------
# Chat Logic
# ----------------------------------

if user_message:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):

        st.write(user_message)

    payload = {

        "user_id": "student",

        "session_id": "academic_session",

        "message": user_message

    }

    try:

        with st.chat_message("assistant"):

            with st.spinner("Searching documents..."):

                response = requests.post(

                    f"{BACKEND_URL}/chat",

                    json=payload,

                    timeout=120

                )

                if response.status_code == 200:

                    data = response.json()

                    ai_reply = data.get(
                        "reply",
                        "No response received."
                    )

                    st.write(ai_reply)

                    if "sources" in data and data["sources"]:

                        with st.expander("📄 Sources Used"):

                            for source in data["sources"]:

                                st.write(f"• {source}")

                else:

                    ai_reply = (
                        f"Backend Error ({response.status_code})"
                    )

                    st.error(ai_reply)

    except Exception as e:

        ai_reply = str(e)

        with st.chat_message("assistant"):

            st.error(ai_reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )
