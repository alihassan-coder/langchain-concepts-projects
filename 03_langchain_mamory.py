from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv  
import os
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

memory1 = ConversationBufferMemory()
memory2 = ConversationBufferWindowMemory(k = 2)
memory3 = ConversationSummaryMemory(llm=llm)
memory4 = ConversationSummaryBufferMemory(llm=llm, max_token_limit=1000)

# Put here the memory which one you want to use
chain = ConversationChain(llm=llm, memory=memory1)

while True: 
    user_input = input("You: ")
    if user_input == "exit":
        print("Exiting the conversation memory1", memory1)
        print("======================")
        print("Exiting the conversation memory2", memory2)
        print("======================")
        print("Exiting the conversation memory3", memory3)
        print("======================")
        print("Exiting the conversation memory4", memory4)
        print("Exiting the conversation.")
        break
    response = chain.invoke(user_input)
    print("Final==>>",response)


