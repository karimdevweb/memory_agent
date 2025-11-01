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

