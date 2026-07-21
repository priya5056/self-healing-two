import streamlit as st
import requests

# ----------------------------------
# Backend URL
# ----------------------------------

try:
    BACKEND_URL = st.secrets["BACKEND_URL"]
except:
    BACKEND_URL = "http://127.0.0.1:8000"


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

    st.markdown("### You can ask about")

    st.markdown("""
- 📘 Admissions
- 💰 Fee Structure
- 👨‍🏫 Faculty
- 🕒 Batch Timings
- 📅 Academic Calendar
- 📚 Study Materials
- 🎯 NEET Preparation
- 💻 JEE Preparation
""")

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------------
# Header
# ----------------------------------

st.title("🎓 AI Academic Assistant")

st.caption(
    "Ask questions related to admissions, fees, faculty, study materials, "
    "batch timings, academic calendar, NEET and JEE preparation."
)

st.divider()

# ----------------------------------
# Chat History
# ----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            if "sources" in message and message["sources"]:

                with st.expander("📄 Sources Used"):

                    for source in message["sources"]:

                        st.markdown(f"- {source}")

# ----------------------------------
# Chat Input
# ----------------------------------

user_message = st.chat_input("Ask your question...")

# ----------------------------------
# Send Message
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

        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=60
        )

        if response.status_code == 200:

            result = response.json()

            ai_reply = result.get(
                "reply",
                "No response."
            )

            sources = result.get(
                "sources",
                []
            )

        else:

            ai_reply = (
                f"Backend Error ({response.status_code})"
            )

            sources = []

    except Exception as e:

        ai_reply = str(e)

        sources = []

    assistant_message = {
        "role": "assistant",
        "content": ai_reply,
        "sources": sources
    }

    st.session_state.messages.append(
        assistant_message
    )

    with st.chat_message("assistant"):

        st.write(ai_reply)

        if sources:

            with st.expander("📄 Sources Used"):

                for source in sources:

                    st.markdown(f"- {source}")