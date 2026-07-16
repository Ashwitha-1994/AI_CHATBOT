import json

from services.llm_service import generate_response


def summarize_conversation(history):
    """
    Summarize the conversation and extract long-term user memory.
    """

    # Convert conversation history into text
    conversation = ""

    for chat in history:
        conversation += f"{chat['role']}: {chat['message']}\n"

    messages = [

        {
            "role": "system",
            "content": """
You are an AI Memory Engine.

Your task is to extract ONLY important long-term user information.

Read the conversation carefully.

Return ONLY valid JSON.

Do NOT return markdown.

Do NOT use ```json.

Return EXACTLY this format:

{
    "profile": {
        "name": "",
        "location": "",
        "project": "",
        "goal": "",
        "technologies": []
    },
    "summary": ""
}

Rules:

1. Extract the user's name.
2. Extract the user's location.
3. Extract the user's project.
4. Extract the user's goal.
5. Extract technologies mentioned.
6. Ignore temporary conversations.
7. Ignore greetings.
8. Do NOT hallucinate.
9. If information is missing, leave it empty.
10. Summary should be less than 100 words.

Return ONLY JSON.
"""
        },

        {
            "role": "user",
            "content": conversation
        }

    ]

    response = generate_response(messages)

    print("\n===== MEMORY ENGINE RESPONSE =====")
    print(response)
    print("==================================\n")

    try:

        data = json.loads(response)

        profile = data.get("profile", {})

        # Build a consistent summary
        summary = f"""
{profile.get('name', '')} is from {profile.get('location', '')}.

They are working on {profile.get('project', '')}.

Their goal is {profile.get('goal', '')}.

Technologies they know include {", ".join(profile.get('technologies', []))}.
"""

        data["summary"] = " ".join(summary.split())

        return data

    except Exception as e:

        print("Memory JSON Parsing Error:", e)

        return {

            "profile": {

                "name": "",

                "location": "",

                "project": "",

                "goal": "",

                "technologies": []

            },

            "summary": ""

        }