from dotenv import load_dotenv
from google import genai
import os,time

load_dotenv()
key =os.getenv("key")

client = genai.Client(api_key=key)
while True:
    user_input=input("You: ")
    if user_input =="exit!":
            break
    response = client.models.generate_content(model = "gemini-2.5-flash",contents = user_input)
    print(response.text)    
    



