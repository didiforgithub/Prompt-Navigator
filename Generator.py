from ErnieLLM import ErnieLLM
"""
这个部分的代码去写Generate部分，
可以

"""


class LLM():
    def __init__(self, model_series="ernie"):
        pass

    def response(self, prompt):
        import erniebot
        # Set authentication params
        erniebot.api_type = "aistudio"
        erniebot.access_token = "2738c7104bbd096b498bfba0816165e692d8f685"

        # Create a chat completion
        response = erniebot.ChatCompletion.create(model="ernie-bot-4",
                                                  messages=[{
                                                      "role": "user",
                                                      "content": prompt
                                                  }])

        return (response.get_result())


class PromptGenerator:

    def __init__(self, model_series="ernie"):
        if model_series == "ernie":
            self.llm = ErnieLLM()
        else:
            # 这个部分是之后做LLM对比的时候改动的
            self.llm = LLM()

    def generate(self, input_prompt, strategy="zero-shot cot", shot=None):
        """
        :param shot:用户给出的样例，缺省时不可使用few-shot策略
        """
        if strategy == "zero-shot cot":
            zero_shot_cot_prompt = f"""
            你是一个优秀的prompt engineer，你擅长使用zero-shot cot策略改写prompt，最经典的zero-shot cot策略当然是在prompt的末尾加上一句："Take a deep breath and work on this problem step-by-step." 
            但我们需要针对当前任务去设计针对性的prompt，比如对于数学计算任务，输出的step就是运算的中间步骤和运算结构，last-step输出的答案是通过多个step的中间结果计算得到的。
            以下是你需要处理的origin-prompt，其中蕴含着当前任务的特征，你需要充分理解当前任务的特点设计step-by-step的zero-shot cot策略。
            origin-prompt:{input_prompt}
            请你分析你的设计思路，并在最后返回一个json格式的zero-shot cot prompt，格式如下：
            {"{"}
                new_prompt: "你的zero-shot cot prompt",
            {"}"}
            """
            re_prompt = self.llm.response(zero_shot_cot_prompt)
            return re_prompt
        elif strategy == "few-shot cot":
            few_shot_cot_prompt = f"""
            你是一个优秀的prompt engineer，你擅长使用few-shot cot策略改写prompt，最经典的few-shot cot策略当然是在prompt的末尾加上一句"Take a deep breath and work on this problem step-by-step."
            然后将所给的示例进行cot拆解，比如shot="input:(2/2+8*√2)^2 output:129 + 16*√2"，那么你需要在prompt的末尾再加上cot拆解后的cot shot"对于我们所处理的数学问题，比如计算(2/2+8*√2)^2，我们可以将其分解为以下几个步骤：
            1. 2/2 = 1
            2. (2/2 + 8*√2)^2 = (1 + 8*√2)^2
            3. (1 + 8*√2)^2 = 1 + 16*√2 + 128
            4. 1 + 16*√2 + 128 = 129 + 16*√2
            所以最终结果是：129 + 16*√2"
            " 
            但我们需要针对当前任务去设计针对性的prompt，比如对于数学计算任务，输出的step就是运算的中间步骤和运算结构，last-step输出的答案是通过多个step的中间结果计算得到的。
            以下是与当前任务相关的few-shot示例，你可以参考之前所给的cot拆解示例，对当前的few-shot示例给出完成的cot解决方案。
            few-shot:{shot}
            以下是你需要处理的origin-prompt，其中蕴含着当前任务的特征，你需要充分理解当前任务的特点设计step-by-step的few-shot cot策略，然后附上few-shot的cot解决方案，便于LLM更好的理解cot思想。
            origin-prompt:{input_prompt}
            请你分析你的设计思路，并在最后返回一个json格式的few-shot cot prompt，格式如下：
            {"{"}
                new_prompt: "你的few-shot cot prompt" ,
            {"}"}
            """
            re_prompt = self.llm.response(few_shot_cot_prompt)
        elif strategy == "zero-shot contrastive":
            zero_shot_cot_prompt = f""""""
            re_prompt = self.llm.response(zero_shot_cot_prompt)
        # 其他策略
        return re_prompt


if __name__ == "__main__":
    prompt_generator = PromptGenerator(model_series="LLM")
    # print(prompt_generator.generate("如果我和我名义上的妈妈没有血缘关系，那么我妈妈有没有可能不是我外婆的女儿？", "few-shot cot"))
    shot = "input:求直角边长度分别为3和4的直角三角形的面积 output:6"
    print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "zero-shot cot"))
    # print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "few-shot cot"))


# 以下是大致会出现的效果
# 任务分析：
# 当前任务是经典的鸡兔同笼问题。我们需要根据给定的头数和脚数来判断鸡和兔各有多少只。这是一个典型的数学问题，需要我们进行逻辑推理和数学计算。

# zero-shot cot策略设计：
# 对于这种逻辑推理和数学计算任务，我们可以采用逐步推导的方式来引导模型得出答案。我们可以设计以下几个step：

# 1. 假设全是鸡，计算脚的数量。
# 2. 根据实际脚数与假设脚数的差值，推算出兔子的数量。
# 3. 用总头数减去兔子的数量，得到鸡的数量。
# 4. 最后输出鸡和兔的具体数量。

# zero-shot cot策略改写：
# 基于以上分析，我们可以将原始prompt改写为以下形式：

# "想象一下，你有一笼鸡和兔。你知道他们的头共有35个，脚共有94只。首先，假设所有的动物都是鸡，那么脚的数量应该是多少呢？接下来，根据实际的脚数和假设的脚数的差值，你能推算出有多少只兔子吗？然后，用总的头数减去兔子的数量，你就能得到鸡的数量了。最后，深呼吸一下，一步一步地解决这个问题，告诉我鸡和兔各有多少只吧！"
