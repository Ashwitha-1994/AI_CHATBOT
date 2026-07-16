from fastapi import APIRouter
from pydantic import BaseModel

from services.conversation_service import (
    get_conversation_history,
    save_message
)

from services.memory_service import (
    get_memory,
    save_memory
)

from services.summary_service import summarize_conversation

from services.prompt_builder import build_prompt

from services.llm_service import generate_response

from services.sentiment_service import analyze_sentiment

from services.intent_service import detect_intent

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    # -------------------------------
    # Load Memory
    # -------------------------------
    memory = get_memory(request.user_id)

    print("\n========== MEMORY ==========")
    print(memory)
    print("============================\n")

    # -------------------------------
    # Conversation History
    # -------------------------------
    history = get_conversation_history(request.user_id)

    # -------------------------------
    # Sentiment Analysis
    # -------------------------------
    sentiment = analyze_sentiment(request.message)

    print("\n========== SENTIMENT ==========")
    print(sentiment)
    print("================================\n")

    # -------------------------------
    # Intent Detection
    # -------------------------------
    intent = detect_intent(request.message)

    print("\n========== INTENT ==========")
    print(intent)
    print("============================\n")
    use_memory = intent["intent"] == "Personal Memory"

    # -------------------------------
    # Simple Intent Routing
    # -------------------------------

    if intent["intent"] == "Greeting":

        return {
            "response": "Hello! 👋 How can I help you today?",
            "intent": intent["intent"],
            "intent_confidence": intent["score"],
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"]
        }

    if intent["intent"] == "Goodbye":

        return {
            "response": "Goodbye! 👋 Have a wonderful day.",
            "intent": intent["intent"],
            "intent_confidence": intent["score"],
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"]
        }

    

    # -------------------------------
    # Build Prompt
    # -------------------------------
    prompt = build_prompt(
        memory,
        history,
        request.message,
        sentiment,
        use_memory
    )

    # -------------------------------
    # Generate AI Response
    # -------------------------------
    answer = generate_response(prompt)

    if answer is None:
        answer = "Sorry, I couldn't generate a response."

    # -------------------------------
    # Save Conversation
    # -------------------------------
    save_message(
        request.user_id,
        "user",
        request.message
    )

    save_message(
        request.user_id,
        "assistant",
        answer
    )

    # -------------------------------
    # Update Memory Every 10 Messages
    # -------------------------------
    updated_history = get_conversation_history(request.user_id)

    if len(updated_history) >= 10:

        summary = summarize_conversation(updated_history)

        save_memory(
            request.user_id,
            summary["profile"],
            summary["summary"]
        )

    # -------------------------------
    # Final Response
    # -------------------------------
    return {

        "response": answer,

        "intent": intent["intent"],

        "intent_confidence": intent["score"],

        "sentiment": sentiment["label"],

        "confidence": sentiment["score"]

    }