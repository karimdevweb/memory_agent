




# pip install ollama
import ollama

MODEL = "mistral:latest"  # your local Ollama model
conversation_memory = []  # full conversation
summary = ""  # running summary

def summarize_memory(memory):
    """Generate a short summary of conversation memory."""
    if not memory:
        return ""
    
    prompt = (
        "You are an AI that summarizes conversations briefly. "
        "Do NOT add commentary, only summarize facts.\n\n"
        "Conversation:\n" + "\n".join(memory) + "\n\nSummary:"
    )
    
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"].strip()

def chat_with_memory(user_input):
    """Add user input to memory, update summary, and get AI reply."""
    global conversation_memory, summary
    
    # Add user input
    conversation_memory.append(f"User: {user_input}")
    
    # Update summary every time
    summary = summarize_memory(conversation_memory)
    
    # Ask AI to respond, including summary as context
    prompt = f"Conversation summary so far:\n{summary}\nUser said: {user_input}\nRespond as an AI assistant:"
    
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    ai_reply = response["message"]["content"].strip()
    conversation_memory.append(f"AI: {ai_reply}")
    
    return ai_reply

# Example usage
print(chat_with_memory("Je développe un agent d’IA pour Ydays."))
print(chat_with_memory("Rappelle-toi de mon projet."))
print(chat_with_memory("Quels sont les objectifs de mon projet?"))


