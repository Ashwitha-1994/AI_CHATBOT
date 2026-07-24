import sys
import os

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(ROOT_DIR)
import streamlit as st
from streamlit_mic_recorder import mic_recorder
import uuid
import os


from backend.services.whisper_service import speech_to_text
from backend.services.llm_service import generate_response
from backend.services.sentiment_service import analyze_sentiment

from backend.services.conversation_service import (
    get_conversation_history,
    save_message
)

from backend.services.memory_service import (
    get_memory,
    save_memory
)

from backend.services.summary_service import summarize_conversation
from backend.services.prompt_builder import build_prompt


# ---------------- Page Config ----------------

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


st.sidebar.success("Streamlit App Running ✅")


st.sidebar.info("""
### Features

✅ Memory

✅ Sentiment Analysis

✅ Voice Input

✅ Whisper Speech Recognition

✅ OpenRouter LLM

✅ MongoDB Atlas

""")


# ---------------- Title ----------------

st.title("🤖 AI Chatbot")

st.caption(
    "Streamlit + Whisper + MongoDB + Memory + OpenRouter"
)


# ---------------- Session ----------------


if "messages" not in st.session_state:

    st.session_state.messages = []


if "voice_key" not in st.session_state:

    st.session_state.voice_key = 0



# ---------------- Display Messages ----------------


for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])



# =====================================================
# CHAT FUNCTION
# =====================================================

def process_chat(message):


    # Memory

    memory = get_memory(user_id)


    # History

    history = get_conversation_history(user_id)


    # Sentiment

    sentiment = analyze_sentiment(message)



    # Prompt

    prompt = build_prompt(
        memory,
        history,
        message,
        sentiment,
        False
    )


    # LLM

    response = generate_response(prompt)



    if response is None:

        response = "Sorry, I could not answer."



    # Save conversation


    save_message(
        user_id,
        "user",
        message
    )


    save_message(
        user_id,
        "assistant",
        response
    )



    return response




# =====================================================
# VOICE INPUT
# =====================================================


st.divider()

st.subheader("🎤 Voice Chat")


audio = mic_recorder(

    start_prompt="🎤 Start Recording",

    stop_prompt="⏹ Stop Recording",

    key=f"mic_{st.session_state.voice_key}"

)



if audio:


    st.success("Voice Recorded")


    filename = f"temp_{uuid.uuid4()}.wav"


    with open(filename,"wb") as f:

        f.write(audio["bytes"])



    try:


        text = speech_to_text(filename)



        st.info(
            f"🎤 You said: {text}"
        )


        st.session_state.messages.append(
            {
                "role":"user",
                "content":text
            }
        )



        answer = process_chat(text)



        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )


        st.session_state.voice_key += 1


        st.rerun()



    except Exception as e:


        st.error(
            f"Voice Error: {e}"
        )



    finally:


        if os.path.exists(filename):

            os.remove(filename)





# =====================================================
# TEXT CHAT
# =====================================================


prompt = st.chat_input(
    "Ask me anything..."
)



if prompt:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )


    try:


        answer = process_chat(prompt)


        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )


        st.rerun()



    except Exception as e:


        st.error(
            f"Chat Error: {e}"
        )