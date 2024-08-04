from ToolAgents.agents import LlamaAgent
from ToolAgents.provider import LlamaCppSamplingSettings, LlamaCppServerProvider
from ToolAgents.provider import VLLMServerSamplingSettings, \
    VLLMServerProvider
from ToolAgents.utilities import ChatHistory
from example_tools import get_weather_function_tool, calculator_function_tool, current_datetime_function_tool
from code_executer import PythonCodeExecutor, system_message_code_agent, run_code_agent

provider = LlamaCppServerProvider("http://127.0.0.1:8080/")

agent = LlamaAgent(llm_provider=provider, debug_output=True)

settings = LlamaCppSamplingSettings()
settings.temperature = 0.3
settings.top_p = 1.0
settings.top_k = 0
settings.min_p = 0.0
settings.max_tokens = 4096
settings.stop = ["</s>", "<|eom_id|>", "<|eot_id|>", "assistant", "<|start_header_id|>assistant<|end_header_id|>"]

chat_history = ChatHistory()
chat_history.add_system_message(system_message_code_agent + f"""\n\n## Predefined Functions

You have access to the following predefined functions in Python:

```python
{get_weather_function_tool.get_python_documentation()}

{calculator_function_tool.get_python_documentation()}

{current_datetime_function_tool.get_python_documentation()}
```

You can call these predefined functions in Python like this:

```python_interpreter
example_function(example_parameter=10.0)
```
""")

python_code_executor = PythonCodeExecutor([get_weather_function_tool, calculator_function_tool, current_datetime_function_tool])

prompt_function_calling = "Get the current weather in New York in Celsius. Get the current weather in London in Celsius. Get the current weather on the North Pole in Celsius. Calculate 5215 * 6987. Get the current date and time in the format: dd-mm-yyyy hh:mm"

prompt = r"""Create a graph of x^2 + 5 with your Python Code Interpreter and save it as an image."""
prompt2 = r"""Create an interesting and engaging random 3d scatter plot with your Python Code Interpreter and save it as an image."""
prompt3 = r"""Analyze and visualize the dataset "./input.csv" with your Python code interpreter as a interesting and visually appealing scatterplot matrix."""

run_code_agent(agent=agent, settings=settings, chat_history=chat_history, user_input=prompt_function_calling,
               python_code_executor=python_code_executor)

run_code_agent(agent=agent, settings=settings, chat_history=chat_history, user_input=prompt,
               python_code_executor=python_code_executor)
run_code_agent(agent=agent, settings=settings, chat_history=chat_history, user_input=prompt2,
               python_code_executor=python_code_executor)
run_code_agent(agent=agent, settings=settings, chat_history=chat_history, user_input=prompt3,
               python_code_executor=python_code_executor)

chat_history.save_history("./test_chat_history_after_llama.json")
