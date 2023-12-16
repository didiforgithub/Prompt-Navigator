from ErnieLLM import ErnieLLM
import ast
"""
这个部分的代码去写Generate部分，
可以

"""


class PromptGenerator:

    def __init__(self, model_series="ernie"):
        if model_series == "ernie":
            self.llm = ErnieLLM()
        else:
            # 这个部分是之后做LLM对比的时候改动的
            self.llm = ErnieLLM()

    def generate(self, input_prompt, strategy="zero-shot cot"):
        if "few-shot" in strategy:
            if "cot" in strategy:
                prompt_prompt = f"""
                你是一个优秀的prompt engineer，你擅长使用cot策略编写样例来提示LLM进行推理，最经典的cot策略当然是在prompt里直接加上一句："Let's work on this problem step-by-step." 
                但我们需要针对当前任务去设计针对性的prompt，比如对于数学计算任务，输出的step就是运算的中间步骤和运算结构，last-step输出的答案是通过多个step的中间结果计算得到的。
                以下是你需要润色的origin-prompt，其中涉及当前的具体任务。
                origin-prompt:{input_prompt}
                请你联想另一个同类型的”问题-答案“对，对这个任务进行cot拆解分析并且给出完整推理过程（包括答案），在最后返回你设计的cot example，格式如下：
                {"{"}
                    'few_shot_example': '''你的few_shot_example''',
                {"}"}
                注意，你的few_shot_example里不能涉及原问题。
                """
            elif "contrastive" in strategy:
                prompt_prompt = f"""
                你是一个优秀的prompt engineer，你擅长使用contrastive（给出在解决当前任务时比较容易犯下的错误）策略编写样例来提示LLM进行推理，
                比如对于数学计算任务，可以结合实例，先给出几个错误的思路，然后沿着这个思路去推理出显然错误的结果或者中间结果：
                contrastive prompt example:
                "对于(2/2+8*√2)^2"，可能会犯下如下几个操作
                - 如果没有括号，那么就会变成"2/2+8*√2^2，加式右部会被计算成16"。
                - 如果没有保留√2的√的符号，8*√2会被计算成16，最终整个式子被计算成289
                - 如果没有注意括号内的运算顺序，结果极大概率会出错
                以上做法都会导致错误，请你在推理过程中避开这些错误，给出最正确的解答"
                以下是你需要润色的origin-prompt，其中涉及当前的具体任务。
                origin-prompt:{input_prompt}
                请你联想另一个同类型的”问题-答案“对，对这个任务设计一些contrastive错误推理示范并给出答案，请把你设计的contrastive example写进如下的格式中：
                {"{"}
                    'few_shot_example': '''你的few_shot_example''',
                {"}"}
                注意，你的few_shot_example里不能涉及原问题。
                """
            elif "difficulty" in strategy:
                prompt_prompt = f"""
                你是一个优秀的prompt engineer，你擅长使用difficulty（提取任务中的难点并进行分析）策略编写样例来提示LLM进行推理，
                比如对于数学计算任务，可以结合实例给出难点提示：
                difficulty prompt example:
                "对于(2/2+8*√2)^2
                - 出现根号，需要理解带根号的数字的运算规则
                - 出现除号，需要理解除数和被除数的顺序
                - 出现次方，需要理解次方角标数字的意义
                请你在推理时格外留意这些难点，给出准确的推理解答
                "
                以下是你需要润色的origin-prompt，其中涉及当前的具体任务。
                origin-prompt:{input_prompt}
                请你联想另一个同类型的”问题-答案“对，对这个任务进行难点抽取分析并给出答案，请把你设计的difficulty example写进如下的格式中：
                {"{"}
                    'few_shot_example': '''你的few_shot_example''',
                {"}"}
                注意，你的few_shot_example里不能涉及原问题。
                """
            few_shot = self.llm.response(prompt_prompt)
            few_shot = ast.literal_eval("{" + few_shot.split("{")[-1].split("}")[0] + "}")
            few_shot = list(few_shot.values())[0]
        if "cot" in strategy:
            prompt_prompt = f"""
            你是一个优秀的提问者，你擅长使用zero-shot cot策略改写prompt来增强LLM的推理能力，最经典的zero-shot cot策略当然是在prompt里直接加上一句："Let's work on this problem step-by-step." 
            但我们需要针对当前任务去设计针对性的prompt，比如对于数学计算任务，输出的step就是运算的中间步骤和运算结构，last-step输出的答案是通过多个step的中间结果计算得到的。
            以下是你需要润色的origin-prompt，其中涉及当前的具体任务，你需要充分理解当前任务的特点设计step-by-step的zero-shot cot策略，但千万不要直接给出答案。
            origin-prompt:{input_prompt}
            请你分析你的设计思路，在最后返回你润色后的zero-shot cot prompt，格式如下：
            {"{"}
                'new_prompt': '''你的zero-shot cot prompt''',
            {"}"}
            """
        elif "contrastive" in strategy:
            prompt_prompt = f"""
            你是一个优秀的提问者，你擅长使用contrastive（给出在解决当前任务时比较容易犯下的错误）策略改写prompt来增强LLM的推理能力，
            比如对于数学计算任务，可以结合实例，先给出几个错误的思路，然后沿着这个思路去推理出显然错误的结果或者中间结果：
            contrastive prompt example:
            "对于(2/2+8*√2)^2"，可能会犯下如下几个操作
            - 如果没有括号，那么就会变成"2/2+8*√2^2，加式右部会被计算成16"。
            - 如果没有保留√2的√的符号，8*√2会被计算成16，最终整个式子被计算成289
            - 如果没有注意括号内的运算顺序，结果极大概率会出错
            以上做法都会导致错误，请你在推理过程中避开这些错误，给出最正确的解答"
            以下是你需要润色的origin-prompt，其中涉及当前的具体任务，你需要充分理解当前任务的特点给出zero-shot contrastive策略。
            origin-prompt:{input_prompt}
            请你分析你的设计思路，在最后返回你润色后的contrastive prompt，格式如下：
            {"{"}
                'new_prompt': '''你的contrastive prompt''' ,
            {"}"}
            """
        elif "difficulty" in strategy:
            prompt_prompt = f"""
            你是一个优秀的提问者，你擅长使用difficulty（提取任务中的难点并进行分析）策略改写prompt来增强LLM的推理能力，
            比如对于数学计算任务，可以结合实例给出难点提示：
            difficulty prompt example:
            "对于(2/2+8*√2)^2
            - 出现根号，需要理解带根号的数字的运算规则
            - 出现除号，需要理解除数和被除数的顺序
            - 出现次方，需要理解次方角标数字的意义
            请你在推理时格外留意这些难点，给出准确的推理解答
            "
            以下是你需要润色的origin-prompt，其中涉及当前的具体任务，你需要充分理解当前任务的特点给出difficulty策略。
            origin-prompt:{input_prompt}
            请你分析你的设计思路，在最后返回你润色后的difficulty prompt，格式如下：
            {"{"}
                'new_prompt': '''你的difficulty prompt''' ,
            {"}"}
            """
        prompt = self.llm.response(prompt_prompt)
        prompt = ast.literal_eval("{" + prompt.split("{")[-1].split("}")[0] + "}")
        prompt = list(prompt.values())[0]
        if "few-shot" in strategy:
            prompt = f"以下是一些推理样例，你可以在后续的推理过程中借鉴：\n{few_shot}\n" + f"请你借鉴以上样例，对下列内容进行思考：\n{prompt}\n" 
        return prompt


if __name__ == "__main__":
    prompt_generator = PromptGenerator()
    # print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "zero-shot cot"))
    # print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "zero-shot contrastive"))
    # print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "zero-shot difficulty"))

    # print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "few-shot cot"))
    # print("***************")
    # print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "few-shot contrastive"))
    # print("***************")
    # print(prompt_generator.generate("鸡兔同笼，头共35个，脚共94只，求鸡与兔各有多少个头？", "few-shot difficulty"))

    print(prompt_generator.generate("你是一个数学大师", "zero-shot cot"))
    print("***************")
    print(prompt_generator.generate("你是一个数学大师", "zero-shot contrastive"))
    print("***************")
    print(prompt_generator.generate("你是一个数学大师", "zero-shot difficulty"))
    print("***************")

    print(prompt_generator.generate("你是一个数学大师", "few-shot cot"))
    print("***************")
    print(prompt_generator.generate("你是一个数学大师", "few-shot contrastive"))
    print("***************")
    print(prompt_generator.generate("你是一个数学大师", "few-shot difficulty"))
