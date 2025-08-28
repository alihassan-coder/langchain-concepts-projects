from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.runnables import RunnableSequence
import os
from dotenv import load_dotenv
load_dotenv()
from requests import request
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

prompt_template = PromptTemplate(
    input_variables=["input"],
    template="You are a tool caller, you have to call the the tool named add_numbers_tool in case if there is any addition required, please don't send any explanation while calling the function, just send the two numbers what users provided e.g 5,2, even though user give the the sentance you have to find two numbers and pass to the functions, user input is: {input}\n")


@tool
def get_weather_tool(city: str) -> str:
    """ Get the weather of a city """
    print("get_weather_tool input_data",city)
    output = request(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=API_KEY")    
    return output

@tool
def add_numbers_tool(input_data: str) -> str:
    """ addition of two numbers. """
    print("add_numbers_tool input_data",input_data)
    try:
        numbers = input_data.split(',')
    except Exception as e:
        return "No numbers found"
    num1, num2 = int(numbers[0]), int(numbers[1])   
    result = num1 + num2
    return f"The Sum of {num1} and {num2} is {result}"

@tool
def multiply_tool(input_data: str) -> str:
    """ Multipy of two numbers """
    print("multiply_tool input_data",input_data)    
    return "Multiplication is 15"
    

chain = RunnableSequence(
    prompt_template, 
    llm,
    get_weather_tool
    )

output = chain.invoke("my first number is 10 and second should be minus of first number by 2")
print("output",output)
    
