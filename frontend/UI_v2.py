import streamlit as st
import requests
st.title("🚀 VERSION 22 JULY DEBUG")
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

    st.subheader("Ask About")

    st.markdown("""
- Admissions
- Fee Structure
- Faculty Information
- Academic Calendar
- Student Policies
- Scholarships
- JEE Preparation
- NEET Preparation
- Study Material
- Batch Timings
""")

    st.markdown("---")

    # Test Backend
    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=5)

        if health.status_code == 200:
            st.success("🟢 Backend Connected")
        else:
            st.error("🔴 Backend Not Healthy")
    except Exception as e:
        st.error("🔴 Backend Offline")
        st.caption(str(e))

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------------
# Header
# ----------------------------------

st.title("🎓 AI Academic Assistant")

st.write(
"""
Welcome!

Ask anything related to:

- Admissions
- Fees
- Scholarships
- Faculty
- Academic Calendar
- Student Policies
- JEE Preparation
- NEET Preparation
- Study Materials
"""
)

# ----------------------------------
# Show Chat History
# ----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# ----------------------------------
# Chat Input
# ----------------------------------

user_message = st.chat_input("Ask your question...")

# ----------------------------------
# Handle Chat
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

    url = f"{BACKEND_URL}/chat"

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    url,
                    json=payload,
                    timeout=120
                )

                # Debug info
                st.caption(f"Calling: {url}")
                st.caption(f"Status Code: {response.status_code}")

                if response.status_code == 200:

                    data = response.json()

                    ai_reply = data.get("reply", "No reply received.")

                    st.write(ai_reply)

                    # Optional Sources
                    if "sources" in data and data["sources"]:
                        st.markdown("### 📄 Sources")
                        for source in data["sources"]:
                            st.write(f"• {source}")

                else:

                    ai_reply = (
                        f"Backend Error ({response.status_code})\n\n"
                        f"{response.text}"
                    )

                    st.error(ai_reply)

            except Exception as e:

                ai_reply = str(e)

                st.error(ai_reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )