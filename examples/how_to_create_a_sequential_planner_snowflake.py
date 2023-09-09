import asyncio

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import OpenAIChatCompletion
from semantic_kernel.planning import SequentialPlanner

from skills.snowflake_operations import SnowflakeOperations

with open("./prompts/sk_seq_prompt", "r") as f:
    PROMPT = f.read()

kernel = sk.Kernel()

api_key, org_id = sk.openai_settings_from_dot_env()
kernel.add_chat_service("gpt-3.5", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))
skills_directory = "../skills/"
snowflake_skill = kernel.import_semantic_skill_from_directory(skills_directory, "DatabaseSkill")
snowflake_query_execute_skill = kernel.import_skill(SnowflakeOperations(),"SnowflakeOperations")
promotion_skill = kernel.import_semantic_skill_from_directory(skills_directory,"PromotionSkill")
ask = """
I want to get a list of customer name who are at the risk of churn.
My customers are in a snowflake database. 
Please create and execute snowflake query to get the customer information. After that write a 
personalized email to the customer to inform about or new promotion."""


planner = SequentialPlanner(kernel,prompt=PROMPT)

sequential_plan = asyncio.run(planner.create_plan_async(goal=ask))

# for step in sequential_plan._steps:
#     print(step.description, ":", step._state.__dict__)

result = asyncio.run(sequential_plan.invoke_async())
print("final result is \n\n", result)
