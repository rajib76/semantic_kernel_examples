from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.sk_pydantic import PydanticField
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter


class IdentifyPrime(PydanticField):
    @sk_function(description="Identifies if a number is prime", name="identify_prime_number")
    # @sk_function_context_parameter(
    #     name="number",
    #     description="number to check if prime",
    # )
    def identify_prime_number(self, context: SKContext) -> str:
        """
        Determines if the number is prime

        Example:
            SKContext["number"] = 21
            {{$number}} => 21 is not a prime number
        """
        # Initializing the prime flag

        number = context["number"]
        prime_flag = "The number {number} is prime".format(number=number)
        if number == 1:
            # 1 is not a prime number
            prime_flag = "The number {number} is not prime".format(number=number)
        elif number > 1:
            # check if number is divisible by any number
            for i in range(2, number):
                if (number % i) == 0:
                    # if divisible, set flag to False
                    prime_flag = "The number {number} is not prime".format(number=number)
                    # and come out of the loop
                    break
        return prime_flag
