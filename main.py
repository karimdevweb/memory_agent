

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



# _____________________________________________ labo 2 mémoire à court terme ____________________________________________________

# try an agent with a conversational memory 
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


# 1. Create model / using ollama because i din't have openai api key
llm = ChatOllama(model="mistral:latest")

# 2. Prompt with memory placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es l'idiot du vilalge."),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])

# 3. Build chain
chain = prompt | llm

# 4. Use a single memory for the whole conversation
memory = ChatMessageHistory()

# 5. Wrap with memory
chat = RunnableWithMessageHistory(
    chain,
    lambda _: memory,
    input_messages_key="input",
    history_messages_key="history"
)
# 5. Config with a session_id (mandatory)
config = {"configurable": {"session_id": "default"}}

# 6. Chat like before
print(chat.invoke({"input": "Bonjour, je m'appelle bob."}, config=config).content)
print(chat.invoke({"input": "Quel est mon nom ?"}, config=config).content)
print(chat.invoke({"input": "si tu te souviens, ajoute kiko à mon nom"}, config=config).content)





# _____________________________________________ labo 3 Mémoire à long terme (Vector Store) _____________________________________________________



# try an agent with a conversational memory 
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory





# add and call back some memories
#  since i have a local ollama, i will use it, openai requires api key
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="Mistral:latest")
store = Chroma(collection_name="memo", embedding_function=embeddings) 
# assigne value to query
while True:
    query = input("Vous : ")
    if query.lower() in ["quit", "exit"]:
            print("Fin du chat. À bientôt !")
            break
    # check if we have to store or recall a memory
    if "souviens-toi" in query: 
        store.add_texts([query]) 
    elif "rappelle-moi" in query:
        results = store.similarity_search_with_score(query, k=1)
        for doc, score in results:
            print("Robot : " , doc.page_content)
                




# _____________________________________________ labo 4 Mémoire résumée (Summarization Memory) _____________________________________________________
