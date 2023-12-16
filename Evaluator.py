import re
from LLM import ErnieLLM, OpenAILLM, Llama


def extract_dict(text):
    pattern = r'\{[^}]*\}'
    matches = re.findall(pattern, text)
    if not matches:
        raise ValueError("No dictionary found in the text.")

    result_dict = eval(matches[0])
    return result_dict


class Evaluator:
    def __init__(self, model_series="ernie-bot-4"):
        if model_series == "ernie-bot-4":
            self.llm = ErnieLLM()
        elif model_series == "gpt-3.5-turbo":
            self.llm = OpenAILLM()
        elif model_series == "llama-7b":
            self.llm = Llama()

    def evaluate(self, question, answer_dict):
        # 输入进来一个Dict，给一个相同Dict的输出，以百分制
        evaluate_prompt = f"""
        你是一个优秀的评估者，你擅长对一个问题的多种答案进行评估，并给出这些答案的分数。
        你将收到一个问题与一个针对这个问题回答的答案的字典，其中键是生成这个问题对应答案的策略，值是答案。
        一个可以参考的例子是
        question:"鸡和兔共49只，一共有100条腿，问鸡和兔各有多少只？"
        {{
        "zero-shot cot": "answer",
        "few-shot cot":"answer"
        }}
        你的评估标准包括答案的正确性、推理的顺畅程度、回答的专业性、回答
        请你使用JSON格式返回一个字典，键为策略，值为一个列表，第一个元素是对应的百分制分数，第二个元素是给出这个分数的原因。
        一个可以参考的例子是
        {{
        "zero-shot cot": ["score","reason"],
        "few-shot cot": ["score","reason"]
        }}
        接下来，你将收到问题与对应的答案字典：
        问题：{question}
        答案字典：{answer_dict}
        """
        eval_result = extract_dict(self.llm.response(evaluate_prompt))
        return eval_result


if __name__ == "__main__":
    evaluator = Evaluator()
    question = "有若干只鸡兔同在一个笼子里，从上面数，有35个头，从下面数，有94只脚。问笼中各有多少只鸡和兔？"
    answer_dict = {}
    result = evaluator.evaluate(question, answer_dict)
    print(result)
    print(extract_dict(result))
    for i in extract_dict(result):
        print(i)
