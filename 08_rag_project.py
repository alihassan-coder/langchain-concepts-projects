import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.indexes import VectorstoreIndexCreator
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from termcolor import colored

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate API key
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in your .env file")

# Initialize LLM and Memory
llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY
)
memory = ConversationBufferWindowMemory(k=5)

# Load all .txt files from /data folder
def load_documents(folder_path="data"):
    loaders = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            full_path = os.path.join(folder_path, file)
            try:
                loaders.append(TextLoader(full_path))
                print(colored(f"Loaded: {file}", "green"))
            except Exception as e:
                print(colored(f"Failed to load {file}: {e}", "red"))
    return loaders

# Create the vector store index
def create_index(loaders):
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    index_creator = VectorstoreIndexCreator(
        embedding=embedding,
        text_splitter=text_splitter
    )
    return index_creator.from_loaders(loaders)

# Main RAG Chat loop
def rag_chat():
    print(colored("Initializing your Gemini RAG Assistant... 🧠", "cyan"))
    
    loaders = load_documents()
    if not loaders:
        raise ValueError("No .txt files found in /data folder.")

    store = create_index(loaders)
    print(colored("Ready to chat! Type 'exit' to quit.", "cyan"))

    while True:
        query = input(colored("\nYou: ", "yellow")).strip()
        if query.lower() in {"exit", "quit"}:
            print(colored("Goodbye! 👋", "green"))
            break
        try:
            response = store.query(query, llm=llm, memory=memory)
            print(colored("Gemini:", "blue"), response)
        except Exception as e:
            print(colored(f"Error: {e}", "red"))

if __name__ == "__main__":
    rag_chat()
