from dotenv import load_dotenv
from google import genai
from google.genai import types
from database import save_messages,init_db,load_messages,delete_messages
from tools.declaration import web_search_tool_config
import os,asyncio
from tools.web_search import web_search



load_dotenv()
key =os.getenv("key2")

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
                           history=history,
                           config = {
                               "tools":[web_search_tool_config]
                           })

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
        chat = client.chats.create(model="gemini-3.6-flash",
                                   config ={"tools":[web_search_tool_config]
                                            })
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
        response = chat.send_message(message=prompt)

        for _ in range(3):
            function_call = None
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_call = part.function_call
                    break

            if not function_call:
                break

            query = function_call.args['query']
            print(f"searching for {query}")
            result = asyncio.run(web_search(query))

            function_response_part = types.Part.from_function_response(
                name=function_call.name,
                response={"result": result}
            )
 
            # sending result back WITH an explicit instruction
            response = chat.send_message(
                message=[
                    function_response_part,
                    "Answer the user's original question now using the search results above. Only search again if these results are truly irrelevant or empty."
                ]
            )

        full_text = response.text

        if full_text is None:
            # loop exhausted, model still hadn't answered — force it, no tools this time
            response = chat.send_message(
                message="Stop searching. Answer the user's question now using only the information already gathered above."
            )
            full_text = response.text or "Sorry, I still couldn't generate an answer."

        print("\nGemini:", full_text)
        save_messages("AI", full_text)

    except Exception as e:
        print(f"\nNETWORK API ERROR OCCURED {e}")
