
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
                