from backend.services.intent_service import detect_intent

print(detect_intent("Hi"))

print(detect_intent("Explain Python"))

print(detect_intent("Tell me about me"))

print(detect_intent("How do I build a CNN?"))

print(detect_intent("Help me prepare for interview"))

print(detect_intent("Bye"))