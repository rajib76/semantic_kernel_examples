# If running from mac execute
# bash /Applications/Python*/Install\ Certificates.command
import semantic_kernel as sk
kernel = sk.Kernel()

from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion

api_key, org_id = sk.openai_settings_from_dot_env()

kernel.add_text_completion_service("OpenAI_davinci", OpenAITextCompletion("text-davinci-003", api_key))
skill = kernel.import_semantic_skill_from_directory("../", "skills")
joke_function = skill["Joke"]
print(joke_function("time travel to dinosaur age"))

