BLOCKED_PATTERNS = [

    "ignore previous",

    "system prompt",

    "reveal prompt",

    "forget previous",

    "api key",

    "developer message",

    "jailbreak"

]


def validate_input(message):

    text = message.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in text:

            return False, "This request is not allowed."

    return True, None