from openai import OpenAI
import ollama
import os
from google import genai
from dotenv import load_dotenv



# _____________________________________________ labo 1 Introduction  + ajout de variable _____________________________________________________



client = OpenAI(
    base_url="http://localhost:11434/v1/",  # Ollama local server
    api_key="ollama",  # obligatoire pour la lib OpenAI, mais ignoré localement
)

def reactive_agent(prompt):
    resp = client.chat.completions.create(
        model="mistral:latest",
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message.content.strip()

print("Tapez 'exit' ou 'quit' pour arrêter.\n")


# add a variabe to show how it could conducte if the agent has a memory
user_name = None 

while True:
    q = input("Vous : ")
    if "je m'appelle" in q.lower(): 
        user_name = q.split()[-1] 
        print(f"Enchanté {user_name} !") 
    elif "mon nom" in q.lower() and user_name: 
        print(f"Tu t'appelles {user_name}.") 
    elif q.lower() in ["quit", "exit"]:
        break
        
    else:
        print("Je ne me souviens pas, désolé.") 
    print("Agent :", reactive_agent(q))


