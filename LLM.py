import erniebot
from openai import OpenAI
import time
import os

"""
文心一言参数：
1. 文心一言API调用自动调用了搜索引擎，使用disable_search才能断掉Search API
2. system，默认False
3. validate_functions，默认False，使用True可以对函数调用进行校验 
"""


class ErnieLLM:
    def __init__(self, model_name="ernie-bot-4", retries=3):
        self.model_name = model_name
        self.retries = retries

    def response(self, query, system=""):
        for i in range(self.retries):
            try:
                time.sleep(0.5)
                response_content = erniebot.ChatCompletion.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": query}],
                    system=system
                )
                return response_content.get_result()
            except Exception as e:
                print(f"{__name__} occurs: {e}")

    def stream_response(self, query, system=""):
        for i in range(self.retries):
            try:
                time.sleep(0.5)
                response_iterator = erniebot.ChatCompletion.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": query}],
                    stream=True,
                    system=system
                )
                for res in response_iterator:
                    yield res.get_result()
            except Exception as e:
                print(f"{__name__} occurs: {e}")

    def multiple_messages_response(self, messages, system=""):
        for i in range(self.retries):
            try:
                time.sleep(0.5)
                response_content = erniebot.ChatCompletion.create(
                    model=self.model_name,
                    messages=messages,
                    system=system
                )
                return response_content.get_result()
            except Exception as e:
                print(f"{__name__} occurs: {e}")


class OpenAILLM():
    def __init__(self, model="gpt-3.5-turbo-1106", temperature=0.7, timeout=60):
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),
                             base_url=os.environ.get("BASE_URL"))

    def response(self, query: str, retries=3):
        for i in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": query}],
                    temperature=self.temperature,
                )
                result = response.choices[0].message.content
                return result
            except Exception as e:
                print(f"{__name__} occurs: {e}")

class Llama:

    # TODO 先不用写长对话，Modify那里长对话都用文心一言，之后有时间再改
    def __init__(self):
        pass

    def response(self):
        pass



if __name__ == "__main__":

    test_chat = ErnieLLM()

    # 完整输出例子
    print(test_chat.response("为我撰写一个关于gradio的300字介绍"))
    # Stream输出例子
    for i in test_chat.stream_response("为我撰写一个关于gradio的300字介绍"):
        print(i, flush=True)
