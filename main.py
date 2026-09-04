from dotenv import load_dotenv
from google import genai
from database import save_messages,init_db,load_messages,delete_messages
import os


load_dotenv()
key =os.getenv("key2")

init_db()
messages = load_messages()
full_text= ""
history = []
#gemini specific history object
for role,content in messages:
    if role=="AI":
        role ="model"
    history.append({"role":role,
                    "parts":[{"text":content}]})
print(history)

client = genai.Client(api_key=key)
chat = client.chats.create(model = "gemini-3.6-flash",
                           history=history)

print("******CLI ASSISTANT********")
print("type /help for commands")

while True:
    user_input=input("You: ")
    if not user_input.strip():
        continue

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
        delete_messages()
        chat = client.chats.create(model="gemini-3.6-flash")
        print("memory cleared")
        continue

    save_messages("user",user_input)
    try:
        response = chat.send_message_stream(message=user_input)
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_text +=chunk.text
        save_messages("AI",full_text)
    
    except Exception as e:
        print(f"\n❌ Network/API Error occurred: {e}")
    