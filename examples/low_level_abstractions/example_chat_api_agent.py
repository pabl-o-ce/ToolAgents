import json
import os

from ToolAgents import ToolRegistry
from ToolAgents.agents import ChatAPIAgent
from ToolAgents.provider import AnthropicChatAPI, AnthropicSettings
from ToolAgents.provider.chat_api_provider import CerebrasChatAPI, CerebrasSettings
from ToolAgents.provider.chat_api_provider.mistral import MistralChatAPI, MistralSettings
from ToolAgents.utilities import ChatHistory
from example_tools import calculator_function_tool, current_datetime_function_tool, get_weather_function_tool

from dotenv import load_dotenv

load_dotenv()

# api = OpenAIChatAPI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1", model="gpt-4-turbo")
# settings = OpenAISettings()

# api = AnthropicChatAPI(api_key=os.getenv("ANTHROPIC_API_KEY"), model="claude-3-5-sonnet-20241022")
# settings = AnthropicSettings()

api = MistralChatAPI(api_key=os.getenv("MISTRAL_API_KEY"), model="mistral-small-latest")
settings = MistralSettings()


# Create the ChatAPIAgent
agent = ChatAPIAgent(chat_api=api, debug_output=True)

settings.temperature = 0.45
settings.top_p = 0.85

# Define the tools
tools = [get_weather_function_tool]
tool_registry = ToolRegistry()

tool_registry.add_tools(tools)
chat_history = ChatHistory()
chat_history.load_history("./test_tools_chat_history.json")

result = agent.get_response(
    messages=chat_history.to_list(),
    settings=settings, tool_registry=tool_registry)

print(result)

chat_history.add_list_of_dicts(agent.last_messages_buffer)
chat_history.save_history("./test_chat_history_after_chat_api.json")