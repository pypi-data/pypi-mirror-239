###### AnyLLM Integration with GPT Cache #########
import gptcache

# openai.ChatCompletion._llm_handler = anyllm.completion
from gptcache.adapter import openai
import dotapi


class AnyLLMChatCompletion(gptcache.adapter.openai.ChatCompletion):
    @classmethod
    def _llm_handler(cls, *llm_args, **llm_kwargs):
        return dotapi.completion(*llm_args, **llm_kwargs)


completion = AnyLLMChatCompletion.create
###### End of AnyLLM Integration with GPT Cache #########


# ####### Example usage ###############
# from gptcache import cache
# completion = AnyLLMChatCompletion.create
# # set API keys in .env / os.environ
# cache.init()
# cache.set_openai_key()
# result = completion(model="claude-2", messages=[{"role": "user", "content": "cto of anyllm"}])
# print(result)
