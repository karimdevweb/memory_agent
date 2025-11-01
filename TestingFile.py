import json
import ollama

MODEL = "Mistral:latest"  # tu peux remplacer par un modèle plus léger
memory_file = "memory.json"

# Charger la mémoire si le fichier existe
try:
    with open(memory_file, "r") as f:
        conversation_memory = json.load(f).get("conversation_memory", [])
except FileNotFoundError:
    conversation_memory = []

def chat_with_memory(user_input):
    global conversation_memory
    conversation_memory.append("User: " + user_input)
    # limiter à 10 derniers messages pour réduire le coût
    if len(conversation_memory) > 10:
        conversation_memory = conversation_memory[-10:]
    prompt = "\n".join(conversation_memory) + "\nUser dit: " + user_input + "\nRéponds comme un assistant :"
    resp = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    ai_reply = resp["message"]["content"].strip()
    conversation_memory.append("AI: " + ai_reply)
    return ai_reply

# -----------------------------
# Menu interactif pour choisir le test
# -----------------------------
while True:
    print("\n===== Tests de mémoire =====")
    print("1 - Recall Test")
    print("2 - Update Test")
    print("3 - Forget Test")
    print("4 - Quitter")
    choice = input("Choisis un test (1-4) : ")

    if choice == "1":
        print("\n--- Recall Test ---")
        chat_with_memory("Mon ami s'appelle Bob")
        chat_with_memory("Salut, ça va ?")
        response = chat_with_memory("Comment s'appelle mon ami ?")
        print("Réponse du Recall Test :", response)

    elif choice == "2":
        print("\n--- Update Test ---")
        response = chat_with_memory("En fait, il s'appelle Marc")
        response = chat_with_memory("Comment s'appelle mon ami ?")
        print("Réponse du Update Test :", response)

    elif choice == "3":
        print("\n--- Forget Test ---")
        response = chat_with_memory("Oublie le nom de mon ami")
        response = chat_with_memory("Comment s'appelle mon ami ?")
        print("Réponse du Forget Test :", response)

    elif choice == "4":
        # Sauvegarde persistante avant de quitter
        with open(memory_file, "w") as f:
            json.dump({"conversation_memory": conversation_memory}, f)
        print("Mémoire sauvegardée. Fin du programme.")
        break

    else:
        print("Choix invalide, réessaie.")
