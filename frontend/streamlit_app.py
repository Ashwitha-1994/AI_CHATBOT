import requests
import streamlit as st
from streamlit_mic_recorder import mic_recorder

API_URL = "https://ai-chatbot-backend-ccem.onrender.com"

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Sidebar ----------------

st.sidebar.title("🤖 AI Chatbot")

user_id = st.sidebar.text_input(
    "User ID",
    value="1009"
)

try:
    health = requests.get(
        API_URL,
        timeout=10
    )

    if health.status_code == 200:
        st.sidebar.success("Backend Connected ✅")
    else:
        st.sidebar.error("Backend Error")

except Exception:
    st.sidebar.error("Backend Offline")

st.sidebar.write(API_URL)
st.sidebar.markdown("---")

st.sidebar.info("""
### Features

✅ Memory

✅ Sentiment

✅ Intent Detection

✅ Voice Input

✅ FastAPI

✅ MongoDB
""")

# ---------------- Title ----------------

st.title("🤖 AI Chatbot")
st.caption("FastAPI + MongoDB + Whisper + Memory + Intent Detection")

# ---------------- Session State ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_key" not in st.session_state:
    st.session_state.voice_key = 0

# ---------------- Display Chat ----------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================================================
# Voice Input
# ======================================================

st.divider()
st.subheader("🎤 Voice Chat")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key=f"mic_{st.session_state.voice_key}"
)

if audio:

    st.success("Voice Recorded")

    files = {
        "audio": (
            "voice.wav",
            audio["bytes"],
            "audio/wav"
        )
    }

    try:

        voice_response = requests.post(
          f"{API_URL}/voice",
          files=files,
          timeout=120
        )

        if voice_response.status_code == 200:

            recognized_text = voice_response.json()["recognized_text"]

            st.info(f"🎤 You said: {recognized_text}")

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": recognized_text
                }
            )

            chat_response = requests.post(
              f"{API_URL}/chat",
              json={
              "user_id": user_id,
              "message": recognized_text
              },
               timeout=120
            ) 

            if chat_response.status_code == 200:

                data = chat_response.json()

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": data["response"]
                    }
                )

                st.session_state.voice_key += 1

                st.rerun()

            else:
                st.error(chat_response.text)

        else:
            st.error("Voice API Error")

    except Exception as e:
        st.error(str(e))

# ======================================================
# Text Input
# ======================================================

prompt = st.chat_input("Ask me anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = requests.post(
      f"{API_URL}/chat",
      json={
        "user_id": user_id,
        "message": prompt
      },
      timeout=120
    )

    if response.status_code == 200:

        data = response.json()

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": data["response"]
            }
        )

        st.rerun()

    else:
        st.error(
            f"Backend Error {response.status_code}: {response.text}"
        )