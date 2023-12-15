from ErnieLLM import ErnieLLM

"""
这个部分的代码去写Generate部分，
可以

"""

class PromptGenerator:
    def __init__(self, strategy = "zero-shot-cot"):
        self.strategy = strategy
        self.llm = ErnieLLM()
    def generate(self, query, system=""):
        response = self.ernie.response(query, system)
        return response["completions"][0]["generated_text"]