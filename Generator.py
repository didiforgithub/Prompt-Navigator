from ErnieLLM import ErnieLLM

"""
这个部分的代码去写Generate部分，
可以

"""

class PromptGenerator:
    def __init__(self,model_series = "ernie"):
        if model_series == "ernie":
            self.llm = ErnieLLM()
        else:
            # 这个部分是之后做LLM对比的时候改动的
            self.llm = ErnieLLM()

    def generate(self, input_prompt, strategy="zero-shot cot"):
        if strategy == "zero-shot cot":
            zero_shot_cot_prompt = f"""
            你是一个优秀的prompt engineer，你擅长使用zero-shot cot策略改写prompt，目前最常用的zero-shot cot提示为：Take a deep breath and work on this problem step-by-step. 
            请你将以下提示词使用zero shot cot策略改写
            origin-prompt:{input_prompt}
            """
            re_prompt = self.llm.response(zero_shot_cot_prompt)
            return re_prompt
        elif strategy == "few-shot cot":
            re_prompt = "helloworld"
            pass
        elif strategy == "self-consistency cot":
            re_prompt = "helloworld"
            pass
        # 其他策略
        return re_prompt

if __name__ == "__main__":
    prompt_generator = PromptGenerator()
    print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？"))