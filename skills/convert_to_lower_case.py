from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.sk_pydantic import PydanticField
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter


class ConvertToLowerCase(PydanticField):
    """
    Description: Converts text to lower case

    Usage:
        kernel.import_skill(ConvertToLowerCase(), skill_name="convert")

    Examples:
        {{convert.convert_to_lower_case}}         => Returns the text to lower case
    """
    @sk_function(
        description="Converts text to lower case",
        name="convert_to_lower_case",
        input_description="The text which needs to be converted",
    )
    @sk_function_context_parameter(
        name="user_input",
        description="the input text that needs to be converted to lower case",
    )
    def convert_to_lower_case(self, user_input:str,context: SKContext) -> str:
        """
        Returns the text in lower case.
        :param input_text: The input text that needs to be converted to lower case
        :param context: Containg the context to get the text from
        :return: The text in lower case
        """
        print("context")
        print(context)
        print("Input text")
        print("inpu ", user_input)
        return user_input.lower()
