import os

from ToolAgents import ToolRegistry
from ToolAgents.agents import ChatToolAgent
from ToolAgents.knowledge.agent_tools.web_search_tool import WebSearchTool
from ToolAgents.messages import ChatMessage

from ToolAgents.provider import AnthropicChatAPI, OpenAIChatAPI
from ToolAgents.knowledge.web_search.implementations.googlesearch import GoogleWebSearchProvider
from ToolAgents.knowledge.web_crawler.implementations.camoufox_crawler import CamoufoxWebCrawler
from dotenv import load_dotenv


load_dotenv()

# Local OpenAI like API, like vllm or llama-cpp-server
# Groq API
api = AnthropicChatAPI(api_key=os.getenv("ANTHROPIC_API_KEY"), model="claude-3-5-sonnet-20241022")
settings = api.get_default_settings()
settings.temperature = 0.45
# Create the ChatAPIAgent
agent = ChatToolAgent(chat_api=api, debug_output=True)
web_crawler = CamoufoxWebCrawler()
web_search_provider = GoogleWebSearchProvider()


summary_api = OpenAIChatAPI(api_key="xxx", base_url="http://127.0.0.1:8080/v1", model="xxx")
summary_settings = summary_api.get_default_settings()
summary_settings.temperature = 0.35
summary_api.set_default_settings(summary_settings)

web_search_tool = WebSearchTool(web_crawler=web_crawler, web_provider=web_search_provider, summarizing_api=summary_api)

tool_registry = ToolRegistry()

tool_registry.add_tool(web_search_tool.get_tool())


messages = [
    ChatMessage.create_system_message("You are a helpful assistant with tool calling capabilities. Only reply with a tool call if the function exists in the library provided by the user. Use JSON format to output your function calls. If it doesn't exist, just reply directly in natural language. When you receive a tool call response, use the output to format an answer to the original user question."),
    ChatMessage.create_user_message("Retrieve latest information about advancements in 3D realtime rendering")
]


chat_response = agent.get_response(
    messages=messages,
    settings=settings, tool_registry=tool_registry)

print(chat_response.response.strip())

print('\n'.join([msg.model_dump_json(indent=4) for msg in chat_response.messages]))