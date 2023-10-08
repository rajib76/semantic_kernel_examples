# This is the logic for the router chain
# The key is the prompt below which does the routing

import json
import re

from chains.base import Chain


class RouterChain(Chain):
    ROUTER_PROMPT_TEMPLATE: str = """
    You are an expert in selecting a prompt name which is best suited for a given raw text input.
    You will be provided a list of prompt names with description of what each prompt is suited for.
    Please revise the original input if you think the revised input will provide a better response.
    Provide your response in a markdown code snippet with a JSON object.

    Here is an example of the output:
    ```json
    {
        "prompt_name": string \\ the prompt name to use or "DEFAULT"
        "modified_input": string \\ the modified version of the original input
    }
    ```
    Always REMEMBER "prompt_name" must be one of the available prompt names given below OR it can be
    "DEFAULT" if the input does not suit any of the provided prompt names.
    The modified_input can be the original input, if no modifications are needed.
    
    [AVAILABLE PROMPTS]
    {{$prompt_names}}
    
    [INPUT]
    {{$input}}
    """

    def __init__(self):
        super().__init__()
        self.module = "RouterChain"

    def run(self,
             prompt_templates,
             input,
             kernel):
        prompt_name_list = {}
        prompt_name_desc={}
        for prompts in prompt_templates:
            name = prompts["prompt_name"]
            prompt_template = prompts["prompt_template"]
            prompt_name_list[name] = prompt_template

        prompt_names = [f"{prompt['prompt_name']}: {prompt['prompt_desc']}" for prompt in prompt_templates]
        prompt_names = prompt_names.__str__()
        print(prompt_names)

        for prompt in prompt_templates:
            prompt_name_desc[prompt['prompt_name']]=prompt['prompt_template']

        sk_context = kernel.create_new_context()
        sk_context["prompt_names"] = prompt_names
        sk_context["input"] = input

        # Instantiate the semantic function
        qa_chat_bot = kernel.create_semantic_function(
            prompt_template=self.ROUTER_PROMPT_TEMPLATE,
            description="Provides a prompt name based on the input question",
            max_tokens=1000
        )

        response = qa_chat_bot.invoke(context=sk_context)

        match = re.search(r"```(json)?(.*)```", str(response), re.DOTALL)
        json_str = match.group(2)
        json_str = json_str.strip()
        parsed_response = json.loads(json_str)
        print("parsed response ", parsed_response)

        prompt = prompt_name_desc[parsed_response['prompt_name']]

        goal = prompt
        print("goal is ", goal)
        input = parsed_response['modified_input']
        print("my inout is ", input)
        return goal,input

