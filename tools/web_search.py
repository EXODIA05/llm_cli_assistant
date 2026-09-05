from dotenv import load_dotenv
import os
from tavily import AsyncTavilyClient
import asyncio

load_dotenv()
tavily = os.getenv("tavily")



async def web_search(query):
    cleaned_result = []
    client = AsyncTavilyClient(api_key=tavily)
    response = await client.search(query)
    result = response.get("results",[])
    if not result:
        return {"message":"NO SEARCH RESULTS FOUND"}
    
    for i in result:
        title = i["title"]
        url = i["url"]
        content = i["content"]
        clean_result = {"title":title,"url":url,"content":content}
        cleaned_result.append(clean_result)
    return cleaned_result 

