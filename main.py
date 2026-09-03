from dotenv import load_dotenv
from google import genai
import os,time

load_dotenv()
key =os.getenv("key")

client = genai.Client(api_key=key)
chat = client.chats.create(model = "gemini-2.5-flash")
print("******CLI ASSISTANT********")
print("type /help for commands")
while True:
    user_input=input("You: ")

    if user_input =="/exit":
        break
    if user_input=="/help":
        print("""
        commands 
        /help = shows commands,
        /exit = exit the llm app,
        /clear = clears the memory
        """)
        continue
        
    if user_input =="/clear":
        chat = client.chats.create(model="gemini-2.5-flash")
        print("memory cleared")
        continue
    response = chat.send_message(message = user_input)
    print(response.text)
    



