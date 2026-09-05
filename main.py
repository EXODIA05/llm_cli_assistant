from dotenv import load_dotenv
from google import genai
from database import save_messages,init_db,load_messages,delete_messages
import os


load_dotenv()
key =os.getenv("key1")

init_db()
messages = load_messages()
history = []
file_context=""

#gemini specific history object
for role,content in messages:
    if role=="AI":
        role ="model"
    history.append({"role":role,""
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
        continue""

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
        file_context=""
        print("memory cleared")
        continue

    if user_input.startswith("/file"):
        file_contents=[]
        parts = user_input.split()
        filename = parts[1]

        if os.path.isfile(filename):
            with open(filename, "r") as f:
                file_contents.append(
            f"\n===== {filename} =====\n{f.read()}"
            )        
        elif os.path.isdir(filename):
            ls = os.listdir(filename)
            print("opening all files and checking its content")
            for i in ls:
                if i.endswith((".py",".md",".txt")):
                    path = os.path.join(filename,i)
                    with open(path,'r') as f:
                        file_contents.append(f"\n{i}-----------\n{f.read()}")
                        
        else:
            print("file/folder doesnt exists")
    
        file_context = "\n".join(file_contents)
        print("loaded succesfully")
        continue

    if file_context:
        prompt = f"""
                    Here is the loaded file/project:
        {file_context}
         User question:       
        {user_input}
    """
    else:
        prompt = user_input

    save_messages("user",user_input)
    try:
        full_text= ""
        response = chat.send_message_stream(message=prompt)
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_text +=chunk.text
        save_messages("AI",full_text)
    
    except Exception as e:
        print(f"\n❌ Network/API Error occurred: {e}")
    