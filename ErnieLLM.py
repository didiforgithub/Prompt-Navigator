import erniebot

"""
文心一言参数：
1. 文心一言API调用自动调用了搜索引擎，使用disable_search才能断掉Search API
2. system，默认False
3. validate_functions，默认False，使用True可以对函数调用进行校验 
"""


class ErnieLLM:
    def __init__(self, model_name="ernie-bot"):
        self.model_name = model_name

    def response(self, query, system=""):
        response_content = erniebot.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": query}],
            system=system
        )
        return response_content.get_result()

    def stream_response(self, query, system=""):
        response_iterator = erniebot.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": query}],
            stream=True,
            system=system
        )
        for res in response_iterator:
            yield res.get_result()

    def multiple_messages_response(self, messages, system=""):
        response_content = erniebot.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            system=system
        )
        return response_content.get_result()


if __name__ == "__main__":

    test_chat = ErnieLLM()

    # 完整输出例子
    print(test_chat.response("为我撰写一个关于gradio的300字介绍"))
    # Stream输出例子
    for i in test_chat.stream_response("为我撰写一个关于gradio的300字介绍"):
        print(i, flush=True)
