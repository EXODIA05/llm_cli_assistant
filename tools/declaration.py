from google.genai import types

web_search_tool = types.FunctionDeclaration(
    name="web_search",
    description="Search the web for current and relevant information.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "query": types.Schema(
                type="STRING",
                description="The search query to use."
            )
        },
        required=["query"]
    )
)

web_search_tool_config = types.Tool(function_declarations=[web_search_tool])
