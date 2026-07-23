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

    st.subheader("Ask About")

    st.markdown("""
- 📌 Admissions
- 💰 Fee Structure
- 👨‍🏫 Faculty Information
- 📅 Academic Calendar
- 📖 Student Policies
- 🎓 Scholarships
- 📚 Study Materials
- 📝 Batch Timings
- 🚀 JEE Preparation
- 🩺 NEET Preparation
""")

    st.markdown("---")

    st.info(
        "💡 Tip:\n\n"
        "Ask complete questions like:\n\n"
        "• What is the JEE fee?\n"
        "• Tell me about scholarships.\n"
        "• Show batch timings."
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ----------------------------------
# Header
# ----------------------------------

st.title("🎓 AI Academic Assistant")

st.markdown(
"""
Welcome!

Ask anything related to:

✅ Admissions

✅ Fee Structure

✅ Scholarships

✅ Faculty Information

✅ Academic Calendar

✅ Student Policies

✅ JEE Preparation

✅ NEET Preparation

✅ Study Materials

---
"""
)

# ----------------------------------
# Display Previous Messages
# ----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# ----------------------------------
# User Input
# ----------------------------------

user_message = st.chat_input(
    "Ask your academic question..."
)

# ----------------------------------
# Handle User Query
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

                if response.status_code == 200:

                    data = response.json()

                    ai_reply = data.get(
                        "reply",
                        "No response received."
                    )

                    st.write(ai_reply)

                    # Display Sources
                    if data.get("sources"):

                        with st.expander(
                            "📄 Sources Used"
                        ):

                            for source in data["sources"]:

                                st.markdown(
                                    f"- **{source}**"
                                )

                else:

                    ai_reply = (
                        f"Backend Error ({response.status_code})"
                    )

                    st.error(ai_reply)

            except requests.exceptions.Timeout:

                ai_reply = (
                    "Request timed out. "
                    "Please try again."
                )

                st.error(ai_reply)

            except requests.exceptions.ConnectionError:

                ai_reply = (
                    "Unable to connect to the backend server."
                )

                st.error(ai_reply)

            except Exception as e:

                ai_reply = (
                    f"Unexpected Error:\n\n{str(e)}"
                )

                st.error(ai_reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )
