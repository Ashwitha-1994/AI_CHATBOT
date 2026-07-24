from fastapi import APIRouter
from pydantic import BaseModel

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
from backend.services.llm_service import generate_response
from backend.services.sentiment_service import analyze_sentiment
# from backend.services.intent_service import detect_intent   # Uncomment if using intent detection

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    print("\n========== NEW CHAT REQUEST ==========")

    # ---------------------------------------------------
    # Step 1 - Memory
    # ---------------------------------------------------
    print("Step 1: Loading Memory...")
    memory = get_memory(request.user_id)

    print("Memory Loaded")
    print(memory)

    # ---------------------------------------------------
    # Step 2 - Conversation History
    # ---------------------------------------------------
    print("Step 2: Loading Conversation History...")
    history = get_conversation_history(request.user_id)

    print(f"History Loaded ({len(history)} messages)")

    # ---------------------------------------------------
    # Step 3 - Sentiment
    # ---------------------------------------------------
    print("Step 3: Running Sentiment Analysis...")

    sentiment = analyze_sentiment(request.message)

    print("Sentiment:")
    print(sentiment)

    # ---------------------------------------------------
    # Step 4 - Intent
    # ---------------------------------------------------
    # Uncomment these lines if your intent model is working

    """
    print("Step 4: Detecting Intent...")

    intent = detect_intent(request.message)

    print(intent)

    use_memory = intent["intent"] == "Personal Memory"

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
    """

    # Temporary intent (recommended while debugging)
    intent = {
        "intent": "General Knowledge",
        "score": 1.0
    }

    use_memory = False

    # ---------------------------------------------------
    # Step 5 - Build Prompt
    # ---------------------------------------------------
    print("Step 5: Building Prompt...")

    prompt = build_prompt(
        memory,
        history,
        request.message,
        sentiment,
        use_memory
    )

    print("Prompt Built Successfully")

    # ---------------------------------------------------
    # Step 6 - LLM
    # ---------------------------------------------------
    print("Step 6: Calling OpenRouter LLM...")

    answer = generate_response(prompt)

    print("LLM Returned:")
    print(answer)

    if answer is None:
        answer = "Sorry, I couldn't generate a response."

    # ---------------------------------------------------
    # Step 7 - Save Conversation
    # ---------------------------------------------------
    print("Step 7: Saving Conversation...")

    # Save user message
    save_message(
        request.user_id,
        "user",
        request.message
    )

    # Don't save OpenRouter/API errors
    if answer.startswith("Error:"):
        print("Skipping error message from conversation history.")
    else:
        save_message(
            request.user_id,
            "assistant",
            answer
        )

    print("Conversation Saved")

    # ---------------------------------------------------
    # Step 8 - Update Long-Term Memory
    # ---------------------------------------------------
    updated_history = get_conversation_history(request.user_id)

    print(f"Conversation Count: {len(updated_history)}")

    if len(updated_history) >= 10:

        print("Generating Conversation Summary...")

        summary = summarize_conversation(updated_history)

        save_memory(
            request.user_id,
            summary["profile"],
            summary["summary"]
        )

        print("Memory Updated Successfully")

    print("========== REQUEST COMPLETED ==========\n")

    # ---------------------------------------------------
    # Final Response
    # ---------------------------------------------------
    return {

        "response": answer,

        "intent": intent["intent"],

        "intent_confidence": intent["score"],

        "sentiment": sentiment["label"],

        "confidence": sentiment["score"]

    }