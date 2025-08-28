from langchain_core.prompts import  ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()


chat_prompt_template = ChatPromptTemplate.from_messages(
    [     
        SystemMessage(content="You are a helpful booking hotel assistant, please response queries about booking hotels."),
    ]
)

llm = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY") 
)



while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    chat_prompt_template.append(HumanMessage(content=user_input))
    chat_prompt = chat_prompt_template.format()
    print("Chat Prompt: ",chat_prompt)
    response = llm.invoke(chat_prompt)
    print("LLM Response",response) 
    chat_prompt_template.append(AIMessage(content=response)) 

