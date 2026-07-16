from openai import OpenAI

from config import (
    OPENROUTER_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def generate_response(messages):

    try:

        print("\n" + "=" * 80)
        print("MODEL :", MODEL_NAME)
        print("=" * 80)

        completion = client.chat.completions.create(

            model=MODEL_NAME,

            messages=messages,

            temperature=TEMPERATURE,

            max_tokens=MAX_TOKENS

        )

        print("\n===== RAW OPENROUTER RESPONSE =====")
        print(completion.model_dump())
        print("==================================\n")

        if not completion.choices:
            return "Sorry, the model returned no choices."

        message = completion.choices[0].message

        content = getattr(message, "content", None)

        # Normal response
        if content is not None:

            if isinstance(content, str):
                return content.strip()

            if isinstance(content, list):

                final_text = ""

                for item in content:

                    if isinstance(item, dict):

                        final_text += item.get("text", "")

                    else:

                        final_text += str(item)

                return final_text.strip()

            return str(content)

        # Reasoning-only models
        reasoning = getattr(message, "reasoning", None)

        if reasoning:

            print("Reasoning:")
            print(reasoning)

            return (
                "The selected model finished its reasoning but did not generate "
                "a final answer. Please try again, increase MAX_TOKENS, "
                "or switch to a chat/instruct model."
            )

        return "The model returned an empty response."

    except Exception as e:

        print("\nLLM ERROR")
        print(e)

        return f"Error: {str(e)}"