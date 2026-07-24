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


router = APIRouter()


class ChatRequest(BaseModel):

    user_id: str
    message: str



@router.post("/chat")
def chat(request: ChatRequest):

    print("\n========== NEW CHAT REQUEST ==========")


    # ===================================================
    # Step 1 - Memory
    # ===================================================

    print("Step 1: Loading Memory...")

    try:

        memory = get_memory(request.user_id)

        print("Memory Loaded")
        print(memory)

    except Exception as e:

        print("Memory Error:", e)

        memory = {
            "profile": {},
            "summary": ""
        }



    # ===================================================
    # Step 2 - Conversation History
    # ===================================================

    print("Step 2: Loading Conversation History...")

    try:

        history = get_conversation_history(
            request.user_id
        )

        print(
            f"History Loaded ({len(history)} messages)"
        )


    except Exception as e:

        print("History Error:", e)

        history = []



    # ===================================================
    # Step 3 - Sentiment
    # ===================================================

    print("Step 3: Running Sentiment Analysis...")


    try:

        sentiment = analyze_sentiment(
            request.message
        )

        print(sentiment)


    except Exception as e:

        print("Sentiment Error:", e)

        sentiment = {

            "label": "NEUTRAL",

            "score": 0.0

        }



    # ===================================================
    # Step 4 - Intent
    # ===================================================

    # Temporary intent
    # Enable intent model later

    intent = {

        "intent": "General Knowledge",

        "score": 1.0

    }


    use_memory = False



    # ===================================================
    # Step 5 - Build Prompt
    # ===================================================


    print("Step 5: Building Prompt...")


    try:

        prompt = build_prompt(

            memory,

            history,

            request.message,

            sentiment,

            use_memory

        )

        print("Prompt Built Successfully")


    except Exception as e:


        print("Prompt Error:", e)

        return {

            "response": "Unable to build prompt",

            "error": str(e)

        }



    # ===================================================
    # Step 6 - LLM Response
    # ===================================================


    print("Step 6: Calling OpenRouter LLM...")


    try:

        answer = generate_response(
            prompt
        )

        print(answer)


    except Exception as e:


        print("LLM Error:", e)

        answer = (
            "Sorry, AI service is temporarily unavailable."
        )



    if answer is None:

        answer = (
            "Sorry, I could not generate a response."
        )



    # ===================================================
    # Step 7 - Save Conversation
    # ===================================================


    print("Step 7: Saving Conversation...")


    try:


        # Save user message

        save_message(

            request.user_id,

            "user",

            request.message

        )


        # Avoid storing API errors

        if answer.startswith("Error:"):

            print(
                "Skipping error message from history."
            )


        else:


            save_message(

                request.user_id,

                "assistant",

                answer

            )


        print("Conversation Saved")


    except Exception as e:


        print(
            "Conversation Save Error:",
            e
        )



    # ===================================================
    # Step 8 - Update Memory Summary
    # ===================================================


    try:


        updated_history = get_conversation_history(
            request.user_id
        )


        print(
            f"Conversation Count: {len(updated_history)}"
        )


        if len(updated_history) >= 10:


            print(
                "Generating Conversation Summary..."
            )


            summary = summarize_conversation(
                updated_history
            )


            save_memory(

                request.user_id,

                summary.get(
                    "profile",
                    {}
                ),

                summary.get(
                    "summary",
                    ""
                )

            )


            print(
                "Memory Updated Successfully"
            )


    except Exception as e:


        print(
            "Summary/Memory Update Error:",
            e
        )



    print(
        "========== REQUEST COMPLETED ==========\n"
    )



    # ===================================================
    # Final Response
    # ===================================================


    return {


        "response": answer,


        "intent": intent["intent"],


        "intent_confidence": intent["score"],


        "sentiment": sentiment["label"],


        "confidence": sentiment["score"]

    }