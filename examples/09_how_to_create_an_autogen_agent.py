import autogen
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-4",
            "gpt4",
            "gpt-4-32k",
            "gpt-4-32k-0314",
            "gpt-4-32k-v0314",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0301",
            "chatgpt-35-turbo-0301",
            "gpt-35-turbo-v0301",
            "gpt",
        }
    }
)

autogen.ChatCompletion.start_logging()

# 1. create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "request_timeout": 600,
        "seed": 42,
        "config_list": config_list,
    }
)

# 2. create the MathUserProxyAgent instance named "mathproxyagent"
# By default, the human_input_mode is "NEVER", which means the agent will not ask for human input.
mathproxyagent = MathUserProxyAgent(
    name="mathproxyagent",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
)
math_problem = "Find all $k$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$. Express your answer in interval " \
               "notation. "
resp = mathproxyagent.initiate_chat(assistant, problem=math_problem)
print(resp)
